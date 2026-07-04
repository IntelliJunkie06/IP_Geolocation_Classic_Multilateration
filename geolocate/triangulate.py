from typing import Sequence, Tuple

import numpy as np
from scipy.optimize import minimize

from .distance import haversine_distance
from .calibration import DEFAULT_SPEED_FACTOR, rtt_to_distance

Point = Tuple[float, float]


def get_search_bounds(
    reference_points: Sequence[Point],
    rtt_values: Sequence[float],
    delta_degrees: float = 4.5,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:

    reference_points = np.asarray(reference_points)
    rtt_values = np.asarray(rtt_values)

    min_rtt_idx = np.argmin(rtt_values)
    min_rtt_point = reference_points[min_rtt_idx]

    lat_bounds = (
        max(min_rtt_point[0] - delta_degrees, -90.0),
        min(min_rtt_point[0] + delta_degrees, 90.0),
    )
    lon_bounds = (
        max(min_rtt_point[1] - delta_degrees, -180.0),
        min(min_rtt_point[1] + delta_degrees, 180.0),
    )

    return lat_bounds, lon_bounds


def triangulation_error(
    guess: Point,
    reference_points: Sequence[Point],
    rtt_values: Sequence[float],
    speed_factor: float = DEFAULT_SPEED_FACTOR,
) -> float:

    lat, lon = guess
    total_error = 0.0
    min_rtt = min(rtt_values)

    for (ref_lat, ref_lon), rtt in zip(reference_points, rtt_values):
        distance = haversine_distance(lat, lon, ref_lat, ref_lon)

        weight = (min_rtt / rtt) ** 2

        expected_distance = rtt_to_distance(rtt, speed_factor)
        error = ((distance - expected_distance) / expected_distance) ** 2

        total_error += error * weight

    return total_error


def locate_device(
    reference_points: Sequence[Point],
    rtt_values: Sequence[float],
    speed_factor: float = DEFAULT_SPEED_FACTOR,
    bound_delta_degrees: float = 4.5,
    maxiter: int = 1000,
) -> np.ndarray:

    reference_points = np.array(reference_points, dtype=float)
    rtt_values = np.array(rtt_values, dtype=float)

    if len(reference_points) != len(rtt_values):
        raise ValueError("reference_points and rtt_values must be the same length")
    if len(reference_points) == 0:
        raise ValueError("need at least one reference point to locate a device")

    min_rtt_idx = np.argmin(rtt_values)
    initial_guess = reference_points[min_rtt_idx]
    lat_bounds, lon_bounds = get_search_bounds(
        reference_points, rtt_values, delta_degrees=bound_delta_degrees
    )

    result = minimize(
        triangulation_error,
        initial_guess,
        args=(reference_points, rtt_values, speed_factor),
        method="L-BFGS-B",
        bounds=[lat_bounds, lon_bounds],
        options={"maxiter": maxiter},
    )

    if not result.success:
        raise ValueError(f"Failed to converge on a solution: {result.message}")

    return result.x