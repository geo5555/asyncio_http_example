import asyncio
import aiohttp
import pprint
import json
import time


async def request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()


async def download_from(q):
    while True:
        url = await q.get()
        if url is None:
            # pass on the word that we're done, and exit
            await q.put(None)
            break
        a = await request(url)
        print(json.loads(a)['id'])


async def main():
    q = asyncio.Queue()
    # create 3 workers
    workers = [asyncio.create_task(download_from(q)) for _ in range(3)]

    urls = [
        f'https://jsonplaceholder.typicode.com/posts/{x}' for x in range(1, 10)]

    for url in urls:
        await q.put(url)
    # Inform the consumers there is no more work.
    await q.put(None)
    await asyncio.wait(workers)


asyncio.run(main())
