from pydantic import BaseModel

from app.models.enums.task import EdgeType


class TaskEdgeCreate(BaseModel):
    depends_on_public_id: int
    edge_type: EdgeType = EdgeType.BLOCKS


class TaskEdgeRead(BaseModel):
    public_id: int
    task_public_id: int
    depends_on_public_id: int
    edge_type: EdgeType

    model_config = {"from_attributes": True}
