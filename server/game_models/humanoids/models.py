import os
import yaml

from game_models.base import BasicModel
from . import constants
from . import exceptions
from . import db_model


class Humanoid(BasicModel):
    KINDS_AVAILABLE = []
    _FIELDS_MAPPING = {
        'kind': str,
        'name': str,
        'age': int,
        'experience': int,
        # пошли хар-ки
        constants.STRENGTH: int,
        constants.AGILITY: int,
        constants.CONSTITUTION: int,
        constants.INTELLIGENCE: int,
        constants.CHARISMA: int,
        constants.WIZDOM: int,
        # прочее
        'free_points': int
    }
    _DB_MODEL = db_model.Humanoid
    BONUS_POINTS = {}
    RACE_NAME = None

    _RESTRICT_LIST_FIELDS = ['id', 'name', 'kind']

    def __init__(self, data=None):
        super().__init__(data=data)
        for stat in constants.STATS:
            setattr(self, stat, constants.BASE_STAT)
        self.free_points = constants.BASE_START_POINTS
        self.experience = 0
        self.kind = self.RACE_NAME

        if data:
            self.fill_data(data)

    def get_stats(self):
        result = {}
        for stat in constants.STATS:
            result[stat] = getattr(self, stat) + self.BONUS_POINTS.get(stat, 0)

        return result

    def to_dict(self):
        result = super().to_dict()
        result.update(self.get_stats())
        return result

    def _get_stat_cost(self, stat_val):
        last_key = 0
        cost = 1
        for k in constants.STAT_UPDATE_ORDER:
            if stat_val < k:
                break
            else:
                last_key = k
        cost = constants.STAT_UPDATE_COST[last_key]

        return cost

    def buy_point(self, stat, amount=1):
        stat_val = getattr(self, stat)
        cost = 0
        for i in range(amount):
            cost += self._get_stat_cost(stat_val+i)
        if self.free_points < cost:
            raise exceptions.NotEnoughPoints('Needed {}, got {}'.format(cost, self.free_points))
        setattr(self, stat, stat_val + amount)
        self.free_points -= cost
        print('Points left: {}'.format(self.free_points))

    @classmethod
    async def get_by_pk(cls, pk):
        db_obj = await cls._get_by_pk(pk)
        if not db_obj:
            return None
        record_cls = cls
        for kind_cls in cls.KINDS_AVAILABLE:
            if getattr(db_obj, 'kind') == kind_cls.RACE_NAME:
                record_cls = kind_cls
                break

        if record_cls.RACE_NAME is None:
            new_race = type(getattr(db_obj, 'kind'), (Humanoid,), {'RACE_NAME': getattr(db_obj, 'kind')})
            Humanoid.KINDS_AVAILABLE.append(new_race)
            record_cls = new_race

        obj = record_cls()
        obj._db_obj = db_obj
        obj._pk = pk
        obj.fill_data_from_db()
        return obj


def create_races():
    AVAILABLE_RACES = {}

    path = os.path.dirname(os.path.abspath(__file__))
    races_file = 'races.yaml'

    with open(os.path.join(path, races_file), 'r') as f:
        races = yaml.safe_load(f)

        for race, params in races.items():
            new_race = type(race, (Humanoid,), params)
            globals()[race] = new_race
            AVAILABLE_RACES[race] = new_race
            Humanoid.KINDS_AVAILABLE.append(new_race)

create_races()
