"""Tests for panel_layout_mock."""

from panel_layout_mock import seed_panels, list_panels, add_panel, remove_panel


def test_seed_panels():
    seed_panels()
    panels = list_panels()
    assert len(panels) == 3
    names = [p["name"] for p in panels]
    assert "Displays" in names
    assert "Views" in names
    assert "Time" in names


def test_add_panel():
    seed_panels()
    assert add_panel("RobotModel", "left") == True
    panels = list_panels()
    assert len(panels) == 4
    assert any(p["name"] == "RobotModel" for p in panels)
    # Duplicate name should fail
    assert add_panel("Displays") == False


def test_remove_panel():
    seed_panels()
    assert remove_panel("Views") == True
    panels = list_panels()
    assert len(panels) == 2
    assert not any(p["name"] == "Views" for p in panels)
    # Remove non-existent panel
    assert remove_panel("NonExistent") == False


def test_add_invalid_name():
    seed_panels()
    assert add_panel("") == False
    assert add_panel(None) == False


test_seed_panels()
