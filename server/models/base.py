import sqlite3

from . import constants


class ValidationError(Exception):
    """Ошибка валидации"""


class NotEnoughPoints(Exception):
    """Не хватает доступных очков"""


class SQLModel:
    _DATABASE = None
    _TABLE = None

    _PYTOSQL_MAPPING = {
        int: 'INTEGER',
        str: 'TEXT',
        float: 'REAL'
    }

    _DEFAULT_SORTING = 'id'
    _RESTRICT_LIST_FIELDS = []

    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)

    @classmethod
    def query(cls, query):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def _create_mapping(cls):
        """
        Здесь мы проверяем существование таблицы
        Если нет - создаем и накатываем поля
        """
        conn = cls._connect()
        cur = conn.cursor()

        query = """
            CREATE TABLE {table} (
                id INTEGER PRIMARY KEY, {fields}
            );
        """.format(
            table=cls._TABLE,
            fields=', '.join([
                "{} {}".format(
                    field,
                    cls._PYTOSQL_MAPPING[
                        cls._FIELDS_MAPPING[field]
                    ]
                ) for field in cls._FIELDS_MAPPING
            ])
        )
        with conn:
            print(query)
            cur.execute(query)

        conn.close()

    def _update_mapping(self):
        """
        Здесь мы проверяем что у нас есть в бд из полей
        Если чего то нет - досоздаем
        """
        pass

    @classmethod
    def _get_by_pk(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT *
                FROM {table}
                WHERE id = :pk
            """.format(table=cls._TABLE),
            {'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        if not record:
            return None
        for idx, col in enumerate(cur.description):
            result[col[0]] = record[idx]
        conn.close()
        return result

    @classmethod
    def get_by_pk(cls, pk):
        record = cls._get_by_pk(pk)
        obj = cls()
        obj.fill_data(record)
        obj._pk = pk
        return obj

    def save(self):
        conn = self._connect()
        cur = conn.cursor()

        with conn:
            fields = list(self._FIELDS_MAPPING.keys())
            vals = [(getattr(self, field)) for field in fields]
            if not self._pk:
                placeholders = ', '.join('?' * len(fields))
                query = """
                    INSERT INTO {table} ({fields}) VALUES ({placeholders})
                """.format(
                    table=self._TABLE,
                    fields=', '.join(fields),
                    placeholders=placeholders,
                )
                cur.execute(query, vals)
            else:
                placeholders = ', '.join([
                    '{}=?'.format(field) for field in fields
                ])
                query = """
                    UPDATE {table} SET {placeholders} WHERE id={pk}
                """.format(
                    table=self._TABLE,
                    placeholders=placeholders,
                    pk=self._pk
                )
                print(query)
                cur.execute(query, vals)
            pk = self._pk or cur.lastrowid
        conn.close()
        return pk

    @classmethod
    def _get_where_clause(cls, **kwargs):
        return ''

    @classmethod
    def get_list(cls, offset=0, limit=10, **kwargs):
        conn = cls._connect()
        cur = conn.cursor()

        sort = kwargs.pop('sort', None)

        cur.execute(
            """
                SELECT *
                FROM {table}
                {where}
                ORDER BY {sort}
                LIMIT {offset}, {limit}
            """.format(
                table=cls._TABLE,
                where=cls._get_where_clause(**kwargs),
                offset=offset,
                limit=limit,
                sort=sort or cls._DEFAULT_SORTING
            )
        )

        result = []
        records = cur.fetchall()
        for record in records:
            result_item = {}
            for idx, col in enumerate(cur.description):
                result_item[col[0]] = record[idx]
            result.append(result_item)

        conn.close()
        return cls._process_search_result(result)

    @classmethod
    def _process_search_result(cls, result):
        if not cls._RESTRICT_LIST_FIELDS:
            return result

        new_result = []
        for record in result:
            new_result.append({
                field: record[field] for field in cls._RESTRICT_LIST_FIELDS
            })

        return new_result


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _DATABASE = 'mydb.db'

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError()

    def fill_data(self, data):
        """
        Args:
            data (dict): данные модели
        """
        for key, val in data.items():
            if self._validate(key, val):
                self.__dict__[key] = val

    def _validate(self, key, val):
        key_type = self._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if key_type != type(val) and val is not None:
            raise ValidationError
        return True

    def to_dict(self):
        inner_dict = {}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, key)
        return inner_dict


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
    _TABLE = 'HumanoidsT'
    BONUS_POINTS = {}
    RACE_NAME = None

    _RESTRICT_LIST_FIELDS = ['id', 'name', 'kind']

    def __init__(self, data=None):
        for stat in constants.STATS:
            setattr(self, stat, constants.BASE_STAT)
        self.free_points = constants.BASE_START_POINTS
        self.experience = 0
        self.kind = self.RACE_NAME
        self._pk = None

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
            raise NotEnoughPoints('Needed {}, got {}'.format(cost, self.free_points))
        setattr(self, stat, stat_val + amount)
        self.free_points -= cost
        print('Points left: {}'.format(self.free_points))

    @classmethod
    def get_by_pk(cls, pk):
        record = cls._get_by_pk(pk)
        if not record:
            return None
        record_cls = cls
        for kind_cls in cls.KINDS_AVAILABLE:
            if record['kind'] == kind_cls.RACE_NAME:
                record_cls = kind_cls
                break

        if record_cls.RACE_NAME is None:
            new_race = type(record['kind'], (Humanoid,), {'RACE_NAME': record['kind']})
            Humanoid.KINDS_AVAILABLE.append(new_race)
            record_cls = new_race

        obj = record_cls()
        obj.fill_data(record)
        obj._pk = pk
        return obj
