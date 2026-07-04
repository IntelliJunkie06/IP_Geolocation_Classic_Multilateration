from pathlib import Path

import numpy as np

from geolocate import (
    haversine_distance,
    load_reference_points,
    locate_device,
)

DATA_DIR = Path(__file__).resolve().parent / "data"
REFERENCE_POINTS_CSV = DATA_DIR / "reference_points.csv"


RTT_VALUES = [
    39.395,  # IN-22
    39.366,  # IN-53
    51.026,  # IN-47
    70.383,  # IN-62
    48.234,  # IN-57
    85.688,  # IN-48
    53.988,  # IN-27
    26.298,  # IN-23
    32.530,  # IN-39
]


def main() -> None:
    landmarks = load_reference_points(REFERENCE_POINTS_CSV)

    if len(landmarks) != len(RTT_VALUES):
        raise ValueError(
            f"Expected {len(landmarks)} RTT values (one per reference point in "
            f"{REFERENCE_POINTS_CSV.name}), got {len(RTT_VALUES)}"
        )

    reference_points = [lp.coords for lp in landmarks]
    rtt_values = RTT_VALUES

    min_rtt_idx = int(np.argmin(rtt_values))
    print(
        f"Reference point with minimum RTT: {landmarks[min_rtt_idx].id} "
        f"{reference_points[min_rtt_idx]} (RTT: {rtt_values[min_rtt_idx]} ms)"
    )

    try:
        lat, lon = locate_device(reference_points, rtt_values)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(f"\nEstimated Location: Latitude = {lat:.6f}, Longitude = {lon:.6f}")

    print("\nVerification:")
    for landmark, rtt in zip(landmarks, rtt_values):
        dist = haversine_distance(lat, lon, landmark.lat, landmark.lon)
        print(f"Distance to {landmark.id}: {dist:.2f} km (RTT: {rtt:.3f} ms)")


if __name__ == "__main__":
    main()