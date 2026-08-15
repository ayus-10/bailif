from uuid import UUID

from pydantic import BaseModel

from app.models.enums.task import DependencyType


class TaskDependencyCreate(BaseModel):
    depends_on_id: UUID
    dependency_type: DependencyType = DependencyType.BLOCKS


class TaskDependencyRead(BaseModel):
    id: UUID
    task_id: UUID
    depends_on_id: UUID
    dependency_type: DependencyType

    model_config = {"from_attributes": True}
