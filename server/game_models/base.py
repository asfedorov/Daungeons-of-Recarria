class ValidationError(Exception):
    """Ошибка валидации"""


class SQLModel:
    _DB_MODEL = None

    _DEFAULT_SORTING = 'id'
    _RESTRICT_LIST_FIELDS = []

    @classmethod
    async def _get_by_pk(cls, pk):
        return await cls._DB_MODEL.get(pk)

    @classmethod
    async def get_by_pk(cls, pk):
        db_obj = await cls._get_by_pk(pk)
        obj = cls()
        obj._db_obj = db_obj
        obj._pk = pk
        return obj

    async def save(self):
        fields = list(self._FIELDS_MAPPING.keys())

        if not self._pk:
            self._db_obj = self._DB_MODEL(**{
                key: getattr(self, key) for key in fields
            })
            await self._db_obj.create()
            self._pk = self._db_obj.id
        else:
            updated = {}
            for field in fields:
                val = getattr(self, field)
                if self._db_obj[field] != val:
                    updated[field] = val
            if updated:
                await self._db_obj.update(**updated).apply()

    @classmethod
    def _get_where_clause(cls, **kwargs):
        return ''

    @classmethod
    async def get_list(cls, offset=0, limit=10, **kwargs):

        sort = kwargs.pop('sort', None)

        result = await cls._DB_MODEL.query.order_by(sort or cls._DEFAULT_SORTING).limit(limit).offset(offset).gino.all()
        return cls._process_search_result(result)

    @classmethod
    def _process_search_result(cls, result):
        if not cls._RESTRICT_LIST_FIELDS:
            return result

        new_result = []
        for record in result:
            new_result.append({
                field: getattr(record, field) for field in cls._RESTRICT_LIST_FIELDS
            })

        return new_result


class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}

    def __init__(self, *args, **kwargs):
        self._pk = None
        self._db_obj = None

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return None
        raise AttributeError()

    @classmethod
    async def get_by_pk(cls, pk):
        obj = super().get_by_pk(pk)
        obj.fill_data_from_db()

    def fill_data_from_db(self):
        self.fill_data(self._db_obj.to_dict())

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
