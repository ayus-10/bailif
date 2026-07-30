import json
import re
from typing import Any

from pydantic import BaseModel, ValidationError


def extract_json(text: str) -> str:
    text = text.strip()
    text = re.sub(
        r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE | re.MULTILINE
    )

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in model output")
    return text[start : end + 1]


def parse_json_raw(raw: str) -> dict[str, Any]:
    try:
        return json.loads(extract_json(raw))
    except json.JSONDecodeError as e:
        raise ValueError("LLM returned invalid JSON") from e


def parse_json[T: BaseModel](raw: str, schema: type[T]) -> T:
    data = parse_json_raw(raw)
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        raise ValueError("LLM JSON did not match expected schema") from e
