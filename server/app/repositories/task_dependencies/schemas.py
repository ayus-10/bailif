from uuid import UUID

from pydantic import BaseModel, model_validator

from app.models.enums.task import DependencyType


class TaskDependencyCreate(BaseModel):
    task_id: UUID
    depends_on_id: UUID
    dependency_type: DependencyType = DependencyType.BLOCKS

    @model_validator(mode="after")
    def validate_not_self_referential(self):
        if self.task_id == self.depends_on_id:
            raise ValueError("a task cannot depend on itself")
        return self


class TaskDependencyRead(BaseModel):
    id: UUID
    task_id: UUID
    depends_on_id: UUID
    dependency_type: DependencyType

    model_config = {"from_attributes": True}
