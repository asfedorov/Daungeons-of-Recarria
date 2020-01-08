import asyncio
from database import db

from settings import get_config
from game_models.humanoids import db_model

db_config = get_config()['postgres']


async def db_update():
    async with db.with_bind(
        'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
    ) as engine:
        await db.gino.create_all()


async def main():
    await db_update()

# if __name__ == '__main__':
asyncio.get_event_loop().run_until_complete(main())
# def create_elf():
#     elf = models.Elf({'name': 'Ara', 'age': 15})
#     elf.save()


# create_elf()
