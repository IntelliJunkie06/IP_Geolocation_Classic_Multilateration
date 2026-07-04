
from typing import Iterable, Sequence, Tuple

from .distance import haversine_distance

DEFAULT_SPEED_FACTOR = 0.2  # km per ms


def rtt_to_distance(rtt: float, speed_factor: float = DEFAULT_SPEED_FACTOR) -> float:

    if rtt <= 0:
        raise ValueError("rtt must be positive")
    return rtt * speed_factor


def calibrate_speed_factor(
    reference_points: Sequence[Tuple[float, float]],
    rtt_values: Sequence[float],
    known_location: Tuple[float, float],
) -> float:
    if len(reference_points) != len(rtt_values):
        raise ValueError("reference_points and rtt_values must be the same length")
    if len(reference_points) == 0:
        raise ValueError("need at least one reference point to calibrate")

    lat0, lon0 = known_location

    numerator = 0.0
    denominator = 0.0
    for (ref_lat, ref_lon), rtt in zip(reference_points, rtt_values):
        distance = haversine_distance(lat0, lon0, ref_lat, ref_lon)
        numerator += distance * rtt
        denominator += rtt * rtt

    if denominator == 0:
        raise ValueError("cannot calibrate: all rtt_values are zero")

    return numerator / denominator