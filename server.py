from aiohttp import web, WSMsgType
import os, pathlib, asyncpg, json, functools

async def database(app):
    app.setdefault('database', await asyncpg.create_pool(host='postgres', user='postgres', database='postgres', password='postgres'))  
    async with app.get('database').acquire() as connection: await connection.execute(pathlib.Path(__file__).resolve().parent.joinpath('database.sql').read_text())
    yield
    async with app.get('database').acquire() as connection: await connection.execute('drop table productItem, productUnit, productReview')
    await app.get('database').close()

async def post(request):
    body = await request.json()
    body = ' '.join(' '.join((key, str(value))) for key,value in body.items())
    async with request.app.get('database').acquire() as connection: records = await connection.fetch(f'select * from{body}')
    return web.json_response([*map(dict, records)], dumps=functools.partial(json.dumps, default=str))

async def websocket(app):
    app.setdefault('websocket', set())
    yield
    for _ in app.get('websocket'): await _.close()
    
async def chat(request):
    websocket = web.WebSocketResponse()
    await websocket.prepare(request)
    websocket.name = await websocket.receive_str()
    for _ in request.app.get('websocket'): await _.send_json({'join':'', 'name':websocket.name})
    request.app.get('websocket').add(websocket)
    async for message in websocket:
        if message.type == WSMsgType.TEXT:
            message = message.json()
            if '' in message:
                for _ in request.app.get('websocket'):
                    if _ is not websocket: await _.send_json({'':message.get(''), 'name':websocket.name})
            elif 'offer' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'offer':message.get('offer'), 'name':websocket.name})
            elif 'answer' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'answer':message.get('answer')})
            elif 'candidate' in message:
                for _ in request.app.get('websocket'):
                    if _.name == message.get('name'): await _.send_json({'candidate':message.get('candidate')})
        else: break
    request.app.get('websocket').discard(websocket)
    for _ in request.app.get('websocket'): await _.send_json({'disconnect':'', 'name':websocket.name})
    return websocket

app = web.Application()
app.add_routes([web.get('/', lambda _: web.FileResponse(pathlib.Path(__file__).resolve().parent / 'index.html')),
                web.post('/ajax', post),
                web.get('/ws', chat),
                web.static('/', pathlib.Path(__file__).resolve().parent)])
app.cleanup_ctx.extend((database, websocket))
web.run_app(app)
