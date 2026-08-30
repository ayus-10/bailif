import base64
from datetime import datetime
from uuid import UUID

from app.core.exceptions import ValidationError


class InvalidCursorError(ValidationError):
    error_code = "invalid_cursor"


def encode_cursor(created_at: datetime, id_: UUID) -> str:
    payload = f"{created_at.isoformat()}|{id_}"
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_cursor(cursor: str) -> tuple[datetime, UUID]:
    try:
        payload = base64.urlsafe_b64decode(cursor.encode()).decode()
        created_at_str, id_str = payload.split("|")
        return datetime.fromisoformat(created_at_str), UUID(id_str)
    except ValueError, TypeError:
        raise InvalidCursorError(cursor)
