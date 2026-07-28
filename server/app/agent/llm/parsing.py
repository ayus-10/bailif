import json

from pydantic import BaseModel, ValidationError


def parse_json[T: BaseModel](raw: str, schema: type[T]) -> T:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("LLM returned invalid JSON") from e

    try:
        return schema.model_validate(data)
    except ValidationError as e:
        raise ValueError("LLM JSON did not match expected schema") from e
