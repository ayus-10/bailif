from datetime import UTC, datetime


def validate_datetime_range(start: datetime | None, end: datetime | None) -> None:
    if start is None or end is None:
        return

    if start.tzinfo is None and end.tzinfo is None:
        start = start.replace(tzinfo=UTC)
        end = end.replace(tzinfo=UTC)
    elif (start.tzinfo is None) != (end.tzinfo is None):
        raise ValueError("end and start must have matching timezone info")

    if end < start:
        raise ValueError("end cannot be before start")
