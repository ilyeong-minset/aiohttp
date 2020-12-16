from aiohttp import web
import pathlib, asyncpg, json
import aredis

async def database(app):
    app.setdefault('database', await asyncpg.create_pool(host='postgres', user='postgres', database='postgres', password='postgres'))
    app.setdefault('cache', aredis.StrictRedis('redis').cache('cache'))
    yield
    await app.get('database').close()

async def post(request):
    body = await request.json()
    body = ' '.join(' '.join((key, str(value))) for key,value in body.items())
    records = await request.app.get('cache').get(body)
    if not records:
        async with request.app.get('database').acquire() as connection: records = json.dumps([*map(dict, await connection.fetch(f'select * from{body}'))], default=str)
        await request.app.get('cache').set(body, records)
    return web.Response(text=records)

app = web.Application()
app.add_routes([web.get('/', lambda _: web.FileResponse(pathlib.Path(__file__).resolve().parent / 'index.html')),
                web.post('/ajax', post),
                web.static('/', pathlib.Path(__file__).resolve().parent)])
app.cleanup_ctx.append(database)
web.run_app(app)
