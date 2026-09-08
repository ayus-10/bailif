from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

SCAN_PATTERNS = {
    "client/src": {
        ".vue": "VUE",
        ".js": "JS",
    },
    "server/app": {
        ".py": "PY",
    },
}


def count_lines_of_code(file_path: Path) -> int:
    """
    Count non-blank lines in a file.

    Lines containing only whitespace are excluded.
    Returns 0 if the file cannot be read.
    """
    try:
        with file_path.open("r", encoding="utf-8", errors="ignore") as file:
            return sum(1 for line in file if line.strip())
    except OSError as exc:
        print(f"Error reading {file_path}: {exc}")
        return 0


def iter_source_files() -> Iterable[tuple[Path, str]]:
    """
    Recursively yield source files and their logical file type.
    """
    for base_path_str, extension_map in SCAN_PATTERNS.items():
        base_path = Path(base_path_str)

        if not base_path.is_dir():
            print(f"Warning: {base_path} not found")
            continue

        for extension, file_type in extension_map.items():
            yield from (
                (file_path, file_type)
                for file_path in base_path.rglob(f"*{extension}")
                if file_path.is_file()
            )


def scan_and_count() -> tuple[list[dict], dict[str, int]]:
    """
    Recursively scan configured directories and count non-blank lines.
    """
    results: list[dict] = []
    totals: dict[str, int] = defaultdict(int)

    for file_path, file_type in iter_source_files():
        loc = count_lines_of_code(file_path)

        results.append(
            {
                "filename": str(file_path),
                "loc": loc,
                "type": file_type,
            }
        )
        totals[file_type] += loc

    return results, totals


def print_results(results: list[dict], totals: dict[str, int]) -> None:
    """
    Print all scan results and summary statistics to console.
    """
    print("\n" + "=" * 80)
    print("CODE METRICS - DETAILED RESULTS")
    print("=" * 80)
    print(f"{'Filename':<60} {'Type':<8} {'LOC':>8}")
    print("-" * 80)

    for result in results:
        filename = result["filename"]
        file_type = result["type"]
        loc = result["loc"]
        print(f"{filename:<60} {file_type:<8} {loc:>8}")

    total_loc = sum(totals.values())

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total files scanned: {len(results)}")
    print("\nLines of Code by Type:")
    print(f"  JavaScript (.js):  {totals.get('JS', 0):,}")
    print(f"  Vue (.vue):        {totals.get('VUE', 0):,}")
    print(f"  Python (.py):      {totals.get('PY', 0):,}")
    print(f"  TOTAL:             {total_loc:,}")
    print("=" * 80)


def main() -> None:
    """
    Run the source-code metrics scanner.
    """
    print("Scanning files for lines of code...")

    results, totals = scan_and_count()

    if not results:
        print("No files found matching the configured patterns.")
        return

    print_results(results, totals)


if __name__ == "__main__":
    main()
