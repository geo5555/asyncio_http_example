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

    for res in asyncio.as_completed(
        (request('https://jsonplaceholder.typicode.com/posts/1'),
         request('https://jsonplaceholder.typicode.com/posts/2'),
         request('https://jsonplaceholder.typicode.com/posts/3'),
         request('https://jsonplaceholder.typicode.com/posts/4'))
    ):
        result = await res
        result = json.loads(result)
        print(f'res: {result["id"]} completed at {time.strftime("%X")}')
    # pprint.pprint{compl}


asyncio.run(main())

# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
#     loop.run_until_complete(loop.shutdown_asyncgens())
# finally:
#     loop.close()
