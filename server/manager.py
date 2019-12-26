import models


def db_update():
    models.Humanoid._create_mapping()


def create_elf():
    elf = models.Elf({'name': 'Ara', 'age': 15})
    elf.save()


create_elf()
