from gino import Gino

db = Gino()

async def init_pg(app):
    db_config = app['config']['postgres']

    engine = await db.set_bind(
        'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
    )
    app['db'] = db
    app['engine'] = engine
