from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from app.agent.schemas.enums import ActionType


class ActionItem(BaseModel):
    type: str
    data: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "ignore"}

    @field_validator("data", mode="before")
    @classmethod
    def default_missing_data(cls, v):
        return v if isinstance(v, dict) else {}


class ActionPlan(BaseModel):
    reply: str = Field(validation_alias="message")
    requires_confirmation: bool = True
    actions: list[ActionItem] = Field(default_factory=list)

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
