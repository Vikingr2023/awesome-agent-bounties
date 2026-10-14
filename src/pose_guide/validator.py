from .models import Pose
import json
from pydantic.error_wrappers import ValidationError

def validate_pose_json(json_data: dict) -> Pose:
    try:
        return Pose.parse_obj(json_data)
    except ValidationError as e:
        raise ValueError(f"Invalid pose schema: {e.json()}") from e
