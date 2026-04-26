from pydantic import BaseModel

class DeliveryTask(BaseModel):
    task_id: str
    origin: str
    destination: str
    estimated_distance: float
