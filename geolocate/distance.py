"""Great-circle distance calculations."""

from math import radians, cos, sin, asin, sqrt

EARTH_RADIUS_KM = 6371.0


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:

    lat1_r, lon1_r, lat2_r, lon2_r = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
    # Clamp to [0, 1] to guard against floating point drift pushing
    # the argument of asin/sqrt slightly out of the valid domain.
    a = max(0.0, min(1.0, a))
    c = 2 * asin(sqrt(a))

    return EARTH_RADIUS_KM * c