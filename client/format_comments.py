from pathlib import Path

SRC_DIR = Path("src")


def process_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    changed = False
    new_lines = []

    for line in lines:
        if "import('" in line:
            new_line = line.replace("'", '"')
            changed |= new_line != line
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed:
        path.write_text("".join(new_lines), encoding="utf-8")
        print(f"Updated: {path}")


for path in SRC_DIR.rglob("*"):
    if path.suffix in {".vue", ".js"}:
        process_file(path)
