import views


def setup_routes(app):
    router = app.router
    router.add_get('/', views.index)

    router.add_get('/humanoids/', views.humanoids)
    router.add_post('/humanoids/', views.humanoids)

    router.add_get('/humanoid/{humanoid_id}/', views.humanoid)
