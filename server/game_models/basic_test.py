import unittest

import races
import constants
from base import Humanoid

def get_races():
    return races.AVAILABLE_RACES


class TestModelsCreations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._expected = [
            'Elf',
            'Human',
            'Dwarf'
        ]

        cls._races = get_races()
        cls._races_names = list(cls._races.keys())

    def test_models_existance(self):
        for race in self._expected:
            self.assertIn(race, self._races)

    def test_models_are_humanoid(self):
        for name, race in self._races.items():
            self.assertTrue(issubclass(race, Humanoid))


class TestHumanoidMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._races = get_races()

    def test_mhumanoid_stats(self):
        for name, race in self._races.items():
            test_obj = race()
            for stat in constants.STATS:
                self.assertIn(stat, test_obj.get_stats())
