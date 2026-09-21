import re
from pathlib import Path

SRC_DIR = Path("src")


def insert_char(value: str, char: str, idx: int) -> str:
    return value[:idx] + char + value[idx:]


def insert_char_from_end(value: str, char: str, idx: int) -> str:
    position = len(value) - idx
    return value[:position] + char + value[position:]


def single_quote_to_double(line: str) -> tuple[str, bool]:
    stripped = line.lstrip()

    if not stripped.startswith(("/*", "*")):
        return line, False

    new_line = re.sub(r"'([^']*)'", r'"\1"', line)

    return new_line, new_line != line


def single_line_to_multi(line: str) -> tuple[str, bool]:
    stripped = line.strip()

    if not (stripped.startswith("/**") and stripped.endswith("*/")):
        return line, False

    processed = insert_char(stripped, "\n *", 3)
    processed = insert_char_from_end(processed, "\n ", 2)

    line_ending = "\n" if line.endswith("\n") else ""
    processed += line_ending

    return processed, True


def is_comment(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(("//", "/*", "*", "*/"))


def ensure_space_between_comment_and_code_snippet(
    line: str,
    prev_line: str | None,
) -> tuple[str, bool]:
    starts_comment = line.lstrip().startswith("/**")
    previous_is_comment = prev_line is not None and is_comment(prev_line)

    if starts_comment and prev_line is not None and not previous_is_comment:
        return "\n" + line, True

    return line, False


def is_redundant_comment_pair(line: str, prev_line: str | None) -> bool:
    return prev_line is not None and line.strip() == "/**" and prev_line.strip() == "*/"


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    changed = False
    new_lines = []

    previous_line = None

    for line in lines:
        if is_redundant_comment_pair(line, previous_line):
            new_lines.pop()

            changed = True
            previous_line = None
            continue

        processed, line_changed = single_line_to_multi(line)
        processed, quote_changed = single_quote_to_double(processed)

        processed, space_added = ensure_space_between_comment_and_code_snippet(
            processed,
            previous_line,
        )

        new_lines.append(processed)

        changed |= line_changed or quote_changed or space_added

        previous_line = processed

    if changed:
        path.write_text("".join(new_lines), encoding="utf-8")
        print(f"Updated: {path}")


for path in SRC_DIR.rglob("*"):
    if path.suffix in {".vue", ".js"}:
        process_file(path)
