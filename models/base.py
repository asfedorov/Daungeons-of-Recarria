import sqlite3


class ValidationError(Exception):
    """Ошибка валидации"""


class SQLModel:
    _DATABASE = None
    _TABLE = None

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

    def _create_mapping(self):
        """
        Здесь мы проверяем существование таблицы
        Если нет - создаем и накатываем поля
        """
        pass

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
                FROM :table
                WHERE id = :pk
            """,
            {'table': cls._TABLE, 'pk': pk}
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col] = record[idx]
        conn.close()
        return result

    @classmethod
    def _get_by_pk_mock(cls, *args):
        return {
            'zaza': 123,
            # 'age': 123,
            'name': 'Iozef'
        }

    @classmethod
    def get_by_pk(cls, pk):
        # record = cls._get_by_pk(pk)
        record = cls._get_by_pk_mock(pk)
        obj = cls()
        obj.fill_data(record)
        return obj


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _INNER_DATA = {}
    _DATABASE = 'mydb.db'

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError()

    # def __setattr__(self, attr, value):
    #   if attr in _FIELDS_MAPPING.keys():
    #       self.__dict__[attr] = value

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
        if key_type != type(val):
            raise ValidationError
        return True

    def to_dict(self):
        inner_dict ={}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, key)
        return inner_dict


class Human(BasicModel):
    _FIELDS_MAPPING = {
        'name': str,
        'age': int
    }
    _TABLE = 'human'

a = Human.get_by_pk(12)

print(a.__dict__)
print(a.to_dict())
