from pydantic import BaseModel, Field


class ChangeProjectRequest(BaseModel):
    id: int = Field(..., gt=0, description="Unical ID of the project")
