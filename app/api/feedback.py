"""Crawler feedback API + learning logic.

Implements:
- GET /api/crawlers/{id}/rewards   -> reward history (source, reason, amount)
- GET /api/crawlers/{id}/feedback   -> accept/reject results
- Learning logic adjusting crawl frequency per source based on adoption rate
- Maintains crawler_stats summary table
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/crawlers", tags=["feedback"])


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

DB_PATH = "crawler_network.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_tables() -> None:
    with get_conn() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS rewards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawler_id TEXT NOT NULL,
                source TEXT NOT NULL,
                reason TEXT,
                amount REAL NOT NULL DEFAULT 0,
                service TEXT,
                info TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crawler_id TEXT NOT NULL,
                source TEXT NOT NULL,
                info TEXT,
                service TEXT,
                accepted INTEGER NOT NULL DEFAULT 0,
                reason TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS crawler_stats (
                crawler_id TEXT NOT NULL,
                source TEXT NOT NULL,
                total INTEGER NOT NULL DEFAULT 0,
                accepted INTEGER NOT NULL DEFAULT 0,
                rejected INTEGER NOT NULL DEFAULT 0,
                adoption_rate REAL NOT NULL DEFAULT 0,
                total_reward REAL NOT NULL DEFAULT 0,
                frequency_weight REAL NOT NULL DEFAULT 1.0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (crawler_id, source)
            );
            """
        )


init_tables()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get("/{crawler_id}/rewards")
def get_rewards(crawler_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT source, reason, amount, service, info, created_at "
            "FROM rewards WHERE crawler_id = ? ORDER BY created_at DESC",
            (crawler_id,),
        ).fetchall()
    if not rows:
        # still valid; return empty list
        pass
    return [dict(r) for r in rows]


@router.get("/{crawler_id}/feedback")
def get_feedback(crawler_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT source, info, service, accepted, reason, created_at "
            "FROM feedback WHERE crawler_id = ? ORDER BY created_at DESC",
            (crawler_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Recording helpers (used by other modules)
# ---------------------------------------------------------------------------


def record_reward(
    crawler_id: str,
    source: str,
    amount: float,
    reason: str = "",
    service: Optional[str] = None,
    info: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO rewards (crawler_id, source, reason, amount, service, info, created_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (crawler_id, source, reason, amount, service, info, datetime.utcnow().isoformat()),
        )
    refresh_stats(crawler_id, source)


def record_feedback(
    crawler_id: str,
    source: str,
    accepted: bool,
    info: Optional[str] = None,
    service: Optional[str] = None,
    reason: Optional[str] = None,
) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO feedback (crawler_id, source, info, service, accepted, reason, created_at) "
            "VALUES (?,?,?,?,?,?,?)",
            (crawler_id, source, info, service, int(accepted), reason, datetime.utcnow().isoformat()),
        )
    refresh_stats(crawler_id, source)


# ---------------------------------------------------------------------------
# Learning logic
# ---------------------------------------------------------------------------


def refresh_stats(crawler_id: str, source: str) -> None:
    """Recompute summary stats for a crawler/source pair and update frequency weight."""
    with get_conn() as conn:
        fb = conn.execute(
            "SELECT COUNT(*) AS total, SUM(accepted) AS acc FROM feedback "
            "WHERE crawler_id=? AND source=?",
            (crawler_id, source),
        ).fetchone()
        rw = conn.execute(
            "SELECT COALESCE(SUM(amount),0) AS amt FROM rewards "
            "WHERE crawler_id=? AND source=?",
            (crawler_id, source),
        ).fetchone()

        total = fb["total"] or 0
        accepted = fb["acc"] or 0
        rejected = total - accepted
        adoption_rate = (accepted / total) if total else 0.0
        total_reward = rw["amt"] or 0.0

        # Frequency weight: high adoption -> increase, low -> decrease.
        # No reward patterns gradually discontinued (weight -> 0).
        if total == 0:
            weight = 1.0
        elif adoption_rate >= 0.7 and total_reward > 0:
            weight = min(2.0, 1.0 + adoption_rate)
        elif adoption_rate < 0.3:
            weight = max(0.1, adoption_rate)
        else:
            weight = 1.0

        # Gradually discontinue patterns with no rewards over time.
        if total >= 5 and total_reward == 0:
            weight = max(0.05, weight * 0.5)

        conn.execute(
            """
            INSERT INTO crawler_stats
                (crawler_id, source, total, accepted, rejected, adoption_rate,
                 total_reward, frequency_weight, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(crawler_id, source) DO UPDATE SET
                total=excluded.total,
                accepted=excluded.accepted,
                rejected=excluded.rejected,
                adoption_rate=excluded.adoption_rate,
                total_reward=excluded.total_reward,
                frequency_weight=excluded.frequency_weight,
                updated_at=excluded.updated_at
            """,
            (
                crawler_id,
                source,
                total,
                accepted,
                rejected,
                adoption_rate,
                total_reward,
                weight,
                datetime.utcnow().isoformat(),
            ),
        )


def get_frequency_weights(crawler_id: str) -> Dict[str, float]:
    """Return per-source frequency weights for a crawler (used by scheduler)."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT source, frequency_weight FROM crawler_stats WHERE crawler_id=?",
            (crawler_id,),
        ).fetchall()
    return {r["source"]: r["frequency_weight"] for r in rows}