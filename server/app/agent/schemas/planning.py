from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from app.agent.schemas.action_items import ActionItemUnion
from app.agent.schemas.enums import ActionType


class ActionPlan(BaseModel):
    reply: str = Field(validation_alias="message")
    requires_confirmation: bool = True
    actions: list[ActionItemUnion] = Field(default_factory=list)

    model_config = {"extra": "ignore", "populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def normalize_reply_key(cls, data: Any) -> Any:
        if isinstance(data, dict) and ("reply" in data and "message" not in data):
            data["message"] = data["reply"]
        return data

    @field_validator("actions", mode="before")
    @classmethod
    def coerce_actions_list(cls, v):
        return v if isinstance(v, list) else []

    @model_validator(mode="after")
    def drop_invalid_action_types(self):
        valid_types = {t.value for t in ActionType}
        self.actions = [a for a in self.actions if a.type in valid_types]
        return self
