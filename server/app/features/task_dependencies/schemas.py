from pydantic import BaseModel

from app.models.enums.task import DependencyType


class TaskDependencyCreate(BaseModel):
    depends_on_public_id: int
    dependency_type: DependencyType = DependencyType.BLOCKS


class TaskDependencyRead(BaseModel):
    public_id: int
    task_public_id: int
    depends_on_public_id: int
    dependency_type: DependencyType

    model_config = {"from_attributes": True}
