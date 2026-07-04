import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest

from geolocate.distance import haversine_distance


class TestHaversineDistance(unittest.TestCase):
    def test_same_point_is_zero(self):
        d = haversine_distance(12.34, 56.78, 12.34, 56.78)
        self.assertAlmostEqual(d, 0.0, places=6)

    def test_known_distance_new_york_los_angeles(self):
        nyc = (40.7128, -74.0060)
        la = (34.0522, -118.2437)
        d = haversine_distance(*nyc, *la)
        self.assertAlmostEqual(d, 3936, delta=20)

    def test_equator_quarter_circumference(self):
        d = haversine_distance(0, 0, 0, 90)
        expected = math.pi * 6371.0 / 2
        self.assertAlmostEqual(d, expected, delta=1)

    def test_antipodal_points(self):
        d = haversine_distance(10, 20, -10, -160)
        expected = math.pi * 6371.0
        self.assertAlmostEqual(d, expected, delta=1)

    def test_symmetry(self):
        d1 = haversine_distance(8.57, 76.87, 17.69, 83.22)
        d2 = haversine_distance(17.69, 83.22, 8.57, 76.87)
        self.assertAlmostEqual(d1, d2, places=9)

    def test_accepts_string_inputs(self):
        d = haversine_distance("8.5692398", "76.8728167", "17.6868159", "83.2184815")
        self.assertGreater(d, 0)


if __name__ == "__main__":
    unittest.main()