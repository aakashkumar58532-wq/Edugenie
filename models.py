from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
