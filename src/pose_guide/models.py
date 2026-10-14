from pydantic import BaseModel
from typing import List

class Joint(BaseModel):
    name: str
    x: float
    y: float
    z: float

class Pose(BaseModel):
    joints: List[Joint]
    tags: List[str]
    standing: bool
