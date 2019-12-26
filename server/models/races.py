import os
import json

from .base import Humanoid

AVAILABLE_RACES = {}

path = os.path.dirname(os.path.abspath(__file__))
races_file = 'races.json'

with open(os.path.join(path, races_file), 'r') as f:
    races = json.load(f)

    for race, params in races.items():
        new_race = type(race, (Humanoid,), params)
        globals()[race] = new_race
        AVAILABLE_RACES[race] = new_race
        Humanoid.KINDS_AVAILABLE.append(new_race)
