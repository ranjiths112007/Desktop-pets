"""Unit test suite for Ben 10 Desktop Pet vector engine."""

import sys
import unittest
from pathlib import Path

# Add root directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ben10_pet import Ben10Pet, Particle


class TestBen10Pet(unittest.TestCase):
    def test_particle_creation(self):
        p = Particle(100.0, 100.0, 1.0, -2.0, 20, 4.0, "#B7FF00")
        self.assertEqual(p.x, 100.0)
        self.assertEqual(p.color, "#B7FF00")


if __name__ == "__main__":
    unittest.main()
