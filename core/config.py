import os
from pydantic import BaseModel

class Settings(BaseModel):
    app_name: str = "Delivery Simulator API"
    debug: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

settings = Settings()
