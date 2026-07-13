"""Mock panel layout manager for RViz-like UI planning.

Provides a simple in-memory store of panels with position metadata.
Default seed panels: Displays (left), Views (right), Time (left).
Supports list, add, and remove operations.
"""

_panels = []


def seed_panels():
    """Seed the initial set of panels."""
    global _panels
    _panels = [
        {"name": "Displays", "position": "left"},
        {"name": "Views", "position": "right"},
        {"name": "Time", "position": "left"},
    ]


def list_panels():
    """Return a list of all panel dictionaries."""
    return list(_panels)


def add_panel(name, position="left"):
    """Add a new panel. Returns True on success, False if name already exists."""
    if not name or not isinstance(name, str):
        return False
    if any(p["name"] == name for p in _panels):
        return False
    _panels.append({"name": name, "position": position})
    return True


def remove_panel(name):
    """Remove a panel by name. Returns True if removed, False if not found."""
    for i, panel in enumerate(_panels):
        if panel["name"] == name:
            _panels.pop(i)
            return True
    return False
