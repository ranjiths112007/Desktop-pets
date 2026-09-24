"""Comprehensive unit test suite for Ben 10 Desktop Pet components."""

import sys
import unittest
from pathlib import Path

# Add root directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from ben10_pet import Ben10PetEngine, Particle, PetState


class TestBen10PetAssets(unittest.TestCase):
    def test_assets_exist(self):
        assets_dir = BASE_DIR / "assets"
        self.assertTrue(assets_dir.exists(), "assets/ directory must exist")

        ben_img = assets_dir / "ben10.png"
        heatblast_img = assets_dir / "heatblast.png"
        self.assertTrue(ben_img.exists(), "assets/ben10.png must exist")
        self.assertTrue(heatblast_img.exists(), "assets/heatblast.png must exist")

    def test_image_loading(self):
        from PIL import Image

        ben_path = BASE_DIR / "assets" / "ben10.png"
        heat_path = BASE_DIR / "assets" / "heatblast.png"

        with Image.open(ben_path) as ben_img:
            self.assertEqual(ben_img.mode, "RGBA")
            self.assertGreater(ben_img.width, 0)

        with Image.open(heat_path) as heat_img:
            self.assertEqual(heat_img.mode, "RGBA")
            self.assertGreater(heat_img.width, 0)

    def test_particle_simulation(self):
        p = Particle(100, 100, 1.0, -2.0, "#b7ff00", 5.0, 10, "spark")
        self.assertTrue(p.update())
        self.assertEqual(p.x, 101.0)
        self.assertEqual(p.y, 98.0)
        self.assertEqual(p.life, 9)

        ember = Particle(50, 50, 0.0, -1.0, "#ff6a00", 6.0, 5, "ember")
        ember.update()
        self.assertLess(ember.radius, 6.0)

    def test_state_enum_coverage(self):
        self.assertIn(PetState.IDLE_BEN, PetState)
        self.assertIn(PetState.ACTIVATE_OMNITRIX, PetState)
        self.assertIn(PetState.TRANSFORMING_TO_HEATBLAST, PetState)
        self.assertIn(PetState.IDLE_HEATBLAST, PetState)
        self.assertIn(PetState.TRANSFORMING_TO_BEN, PetState)


if __name__ == "__main__":
    unittest.main()
