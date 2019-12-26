from aiohttp import web

import models


async def index(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def humanoids(request):
    if request.method == 'POST':
        data = request.json

        humanoid = models.Humanoid(data=data)
        humanoid.save()

    humanoids_list = models.Humanoid.get_list()
    return web.json_response(humanoids_list)


async def humanoid(request):
    if request.method == 'GET':
        humanoid_id = request.match_info.get('humanoid_id')
        humanoid = models.Humanoid.get_by_pk(humanoid_id)
        if humanoid:
            return web.json_response(humanoid.to_dict())
        else:
            return web.json_response({'error': 'no such humanoid'})
