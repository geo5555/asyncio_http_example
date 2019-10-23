import asyncio
from random import randint
import json
import aiohttp
import time


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def safe_download(url,sem):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await download(url)

async def main():
    sem = asyncio.Semaphore(5)
    #loop = asyncio.get_event_loop()
    urls = [
        f'https://jsonplaceholder.typicode.com/posts/{x}' for x in range(1, 10)
        ]

    tasks = [
        #asyncio.ensure_future(safe_download(url)) for url in urls
        asyncio.create_task(safe_download(url,sem)) for url in urls
        ]
    t1 = time.perf_counter()
    for res in asyncio.as_completed(tasks):
        result = await res
        result = json.loads(result)
        t2 = time.perf_counter()
        print(t2-t1)
        print(f'res: {result["id"]} completed at {time.strftime("%X")}')




#I get an error if semaphores are declared outside the main, 
#because asyncio.run() creates a new loop, while semaphores get the events.get_event_loop()
asyncio.run(main())
