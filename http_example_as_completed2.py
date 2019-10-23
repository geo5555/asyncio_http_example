import asyncio
import aiohttp
import pprint
import json
import time


async def request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def main():
    tasks = []
    for i in range(1, 10):
        t1 = asyncio.create_task(
            request(f'https://jsonplaceholder.typicode.com/posts/{i}'))
        tasks.append(t1)

    for res in asyncio.as_completed(
        (tasks)
    ):
        result = await res
        result = json.loads(result)
        print(f'res: {result["id"]} completed at {time.strftime("%X")}')


asyncio.run(main())
