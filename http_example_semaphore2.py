import asyncio
from random import randint
import json
import aiohttp
import time


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            a=await resp.text()
            print(json.loads(a)['id'])
            return a


async def safe_download(url,sem):
    async with sem:  # semaphore limits num of simultaneous downloads
        return await download(url)

async def main():
    sem = asyncio.Semaphore(5)
    urls = [
        f'https://jsonplaceholder.typicode.com/posts/{x}' for x in range(1, 10)
        ]
    tasks = [
        #asyncio.ensure_future(safe_download(url)) for url in urls
        asyncio.create_task(safe_download(url,sem)) for url in urls
        ]
    t1 = time.perf_counter()
    results = await asyncio.gather(*tasks)  # await moment all downloads done
    t2 = time.perf_counter()
    print(t2-t1)
    for result in results:
        result = json.loads(result)
        print(f'res: {result["id"]} completed at {time.strftime("%X")}')


#I get an error if semaphores are declared outside the main, 
#because asyncio.run() creates a new loop, while semaphores get the events.get_event_loop()
asyncio.run(main())
