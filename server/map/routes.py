from . import views


def setup_routes(app):
    router = app.router
    router.add_post('/map/', views.map_index)
