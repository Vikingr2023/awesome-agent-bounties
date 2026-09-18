"""Validation module for RustChain blockchain comparative analyses."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set


@dataclass
class ValidationResult:
    """Outcome of comparison verification.

    Attributes:
        is_valid: Whether all validation criteria passed.
        word_count: Total word count of the analysis.
        missing_sections: Sections required by the specification that are absent.
        missing_terms: Critical technical concepts that are absent.
        errors: Detailed messages describing validation failures.
        metrics: Additional calculated metrics regarding the document.
    """

    is_valid: bool
    word_count: int
    missing_sections: List[str] = field(default_factory=list)
    missing_terms: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)


class ComparisonValidator:
    """Validates markdown comparative analyses against bounty stipulations."""

    REQUIRED_SECTIONS: List[str] = [
        "Consensus Mechanism Differences",
        "Hardware Requirements",
        "Environmental Approach",
        "Community Model and Governance",
        "Comparative Advantages and System Tradeoffs",
    ]

    REQUIRED_KEY_TERMS: Dict[str, List[str]] = {
        "rustchain": ["rustchain", "proof of antiquity", "ram coffers"],
        "comparison_target": ["solana", "proof of history", "tower bft"],
        "consensus": ["consensus", "validator"],
        "environmental": ["environmental", "electronic waste", "energy"],
        "limitations": ["limitations", "short", "throughput", "sybil"],
    }

    def __init__(self, file_path: str | Path) -> None:
        """Initialize validator with target markdown document.

        Args:
            file_path: Filesystem path to markdown document.
        """
        self.file_path = Path(file_path)
        self._cached_content: str | None = None

    def read_content(self) -> str:
        """Read and cache raw markdown content from disk.

        Returns:
            Decoded document text.

        Raises:
            FileNotFoundError: If the document does not exist.
        """
        if self._cached_content is None:
            if not self.file_path.exists():
                raise FileNotFoundError(f"File not found: {self.file_path}")
            self._cached_content = self.file_path.read_text(encoding="utf-8")
        return self._cached_content

    def calculate_word_count(self) -> int:
        """Calculate total word count excluding markdown structural syntax.

        Returns:
            Total count of alphanumeric words in the document body.
        """
        content = self.read_content()
        cleaned_text = re.sub(r"[#*`_>\[\]\(\)\-\|]", " ", content)
        words = [w for w in cleaned_text.split() if w.strip()]
        return len(words)

    def extract_headings(self) -> List[str]:
        """Extract all markdown headings defined in the document.

        Returns:
            List of clean heading names.
        """
        content = self.read_content()
        heading_matches = re.findall(r"^#{1,6}\s+(.+)$", content, flags=re.MULTILINE)
        return [h.strip() for h in heading_matches]

    def verify_required_sections(self) -> List[str]:
        """Verify that all mandatory comparative sections are present.

        Returns:
            List of required section names that are missing.
        """
        headings = self.extract_headings()
        normalized_headings = {h.lower() for h in headings}
        missing: List[str] = []
        for req in self.REQUIRED_SECTIONS:
            if not any(req.lower() in nh for nh in normalized_headings):
                missing.append(req)
        return missing

    def verify_required_terms(self) -> List[str]:
        """Verify that core technical terms and conceptual criteria exist.

        Returns:
            List of concept categories that failed detection.
        """
        content = self.read_content().lower()
        missing_categories: List[str] = []
        for category, terms in self.REQUIRED_KEY_TERMS.items():
            matched = any(term.lower() in content for term in terms)
            if not matched:
                missing_categories.append(category)
        return missing_categories

    def validate(self, min_words: int = 300, max_words: int = 800) -> ValidationResult:
        """Execute full compliance validation against bounty criteria.

        Args:
            min_words: Minimum permissible word count.
            max_words: Maximum permissible word count.

        Returns:
            ValidationResult with detailed status and diagnostics.
        """
        errors: List[str] = []
        word_count = self.calculate_word_count()

        if word_count < min_words:
            errors.append(f"Word count {word_count} is below minimum requirement of {min_words}.")
        elif word_count > max_words:
            errors.append(f"Word count {word_count} exceeds maximum allowance of {max_words}.")

        missing_sections = self.verify_required_sections()
        if missing_sections:
            errors.append(f"Missing required sections: {', '.join(missing_sections)}")

        missing_terms = self.verify_required_terms()
        if missing_terms:
            errors.append(f"Missing required conceptual terms for categories: {', '.join(missing_terms)}")

        headings = self.extract_headings()
        metrics: Dict[str, Any] = {
            "word_count": word_count,
            "heading_count": len(headings),
            "headings": headings,
            "path": str(self.file_path),
        }

        return ValidationResult(
            is_valid=(len(errors) == 0),
            word_count=word_count,
            missing_sections=missing_sections,
            missing_terms=missing_terms,
            errors=errors,
            metrics=metrics,
        )
