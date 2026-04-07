from pydantic import BaseModel
from typing import List, Dict

class Observation(BaseModel):
    logs: str
    metrics: Dict[str, float]
    alerts: List[str]

class Action(BaseModel):
    action: str  # restart_service, scale_up, rollback, ignore

class Reward(BaseModel):
    reward: float