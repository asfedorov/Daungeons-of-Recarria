from aiohttp import web


def json_rpc2_web_response(func):
    async def wrapper(request):
        data = await request.json()
        _id = data.get('id')
        func_result = await func(request)

        result = {
            'jsonrpc': '2.0',
        }
        if _id:
            result['id'] = _id

        if isinstance(func_result, dict):
            if 'error' in func_result or 'result' in func_result:
                result.update(func_result)
            else:
                result['result'] = func_result
        else:
            result['result'] = func_result

        return web.json_response(result)
    return wrapper
