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


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _INNER_DATA = {}
    _DATABASE = 'mydb.db'

    def fill_data(self, data):
        """
        Args:
            data (dict): данные модели
        """
        for key, val in data.items():
            if self._validate(key, val):
                self._INNER_DATA[key] = val

    def _validate(self, key, val):
        key_type = self._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if key_type != type(val):
            raise ValidationError
        return True

    def to_dict(self):
        return self._INNER_DATA


class Human(BasicModel):
    _FIELDS_MAPPING = {
        'name': str,
        'age': int
    }
    _TABLE = 'human'

a = Human()
a.fill_data({
    'zaza': 123,
    'age': 123,
    'name': 'Iozef'
})
print(a.to_dict())
