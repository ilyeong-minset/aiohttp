import aiohttp, asyncio, json, argparse
parser = argparse.ArgumentParser()
parser.add_argument('github')

async def f():
    async with aiohttp.ClientSession() as session:
        for _ in ('vertx', 'koa'): 
            async with session.post(f'https://api.github.com/repos/chaowenGUOorg/{_}/dispatches', data=json.dumps({'event_type':'ping'}).encode(), auth=aiohttp.BasicAuth('chaowenGUO', parser.parse_args().github)) as _: pass

asyncio.run(f())
