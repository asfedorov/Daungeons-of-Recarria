from aiohttp import web
from routes import setup_routes
from settings import get_config
from database import init_pg

app = web.Application()
app.on_startup.append(init_pg)
setup_routes(app)

# set mode='prod' for production config
app['config'] = get_config()

if __name__ == '__main__':
    web.run_app(app)
