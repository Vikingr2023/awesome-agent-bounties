import pytest
from pydantic import ValidationError
from src.pose_guide.models import Pose

valid_pose = {
    "joints": [
        {"name": "head", "x": 0.0, "y": 0.0, "z": 0.0},
        {"name": "neck", "x": 0.0, "y": -3.0, "z": 0.0}
    ],
    "tags": ["standing", "formal"],
    "standing": True
}

invalid_pose_missing_standing = {
    "joints": [
        {"name": "head", "x": 0.0, "y": 0.0, "z": 0.0}
    ],
    "tags": ["sitting"]
}

def test_valid_pose():
    pose = Pose.parse_obj(valid_pose)
    assert len(pose.joints) == 2
    assert "formal" in pose.tags
    assert pose.standing is True

def test_missing_standing_flag():
    with pytest.raises(ValidationError):
        Pose.parse_obj(invalid_pose_missing_standing)

def test_invalid_joint_structure():
    invalid_joint = {
        "joints": [{"name": "hand", "x": "invalid"}],
        "tags": [],
        "standing": False
    }
    with pytest.raises(ValidationError):
        Pose.parse_obj(invalid_joint)
