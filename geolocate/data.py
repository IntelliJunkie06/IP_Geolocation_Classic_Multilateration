import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union


@dataclass(frozen=True)
class ReferencePoint:
    id: str
    lat: float
    lon: float

    @property
    def coords(self) -> tuple:
        return (self.lat, self.lon)


def load_reference_points(csv_path: Union[str, Path]) -> List[ReferencePoint]:
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"reference points file not found: {csv_path}")

    points: List[ReferencePoint] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"id", "lat", "lon"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"CSV must contain columns {required}, got {reader.fieldnames}")

        for row_num, row in enumerate(reader, start=2):  # header is row 1
            try:
                points.append(
                    ReferencePoint(
                        id=row["id"].strip(),
                        lat=float(row["lat"]),
                        lon=float(row["lon"]),
                    )
                )
            except (KeyError, ValueError) as exc:
                raise ValueError(f"malformed row {row_num} in {csv_path}: {row}") from exc

    if not points:
        raise ValueError(f"no reference points found in {csv_path}")

    return points