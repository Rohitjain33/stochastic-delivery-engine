from pydantic import BaseModel, Field
from typing import List


class StageInput(BaseModel):
    name: str
    mean: float = Field(gt=0)
    std: float = Field(ge=0)


class SimulationRequest(BaseModel):
    stages: List[StageInput]
    runs: int = Field(default=10000, gt=0)
    sla: float = Field(gt=0)
    mode: str = "independent"  # allow: independent, random_walk, markov
    traffic_level: str = "normal"


class SimulationResponse(BaseModel):
    expected_time: float
    p95_time: float
    delay_probability: float
    risk_level: str
