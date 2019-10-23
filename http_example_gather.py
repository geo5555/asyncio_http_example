import asyncio
import aiohttp
import pprint
import json


async def request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def main():
    results = await asyncio.gather(
        request('https://jsonplaceholder.typicode.com/posts/1'),
        request('https://jsonplaceholder.typicode.com/posts/2'),
        request('https://jsonplaceholder.typicode.com/posts/3'),
        request('https://jsonplaceholder.typicode.com/posts/4'),
    )
    for item in results:
        item = json.loads(item)
        print(f"{item['id']} of user")

asyncio.run(main())
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
#     loop.run_until_complete(loop.shutdown_asyncgens())
# finally:
#     loop.close()
