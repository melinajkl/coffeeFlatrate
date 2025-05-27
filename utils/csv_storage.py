import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "projekt/data"

def read_csv(file_name: str) -> list[dict]:
    path = DATA_DIR / file_name
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

def write_csv(file_name: str, data: list[dict], fieldnames: list[str]) -> None:
    path = DATA_DIR / file_name
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(file_name: str, row: dict) -> None:
    path = DATA_DIR / file_name
    file_exists = path.exists()
    with open(path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)