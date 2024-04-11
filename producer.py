import asyncio
import aiohttp

class Producer:
    def __init__(self, url_file: str, queue: asyncio.Queue):
        self.url_file = url_file
        self.queue = queue

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> None:
        if (url):
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    item = {'url' : url,
                            'content': html}
                    
                    if self.queue.full():
                        oldest_item = await self.queue.get()
                        print(f"Removed oldest item: {url}")
                    await self.queue.put(item)

            except Exception as e:
                print(f"Error occured while fetching {url}: {str(e)}",)

    async def run(self) -> None:

        async with aiohttp.ClientSession() as session:
            with open(self.url_file, 'r') as file:
                urls = file.readlines()

            tasks = []

            for url in urls:
                url = url.strip()
                task = asyncio.create_task(self.fetch(session, url))
                tasks.append(task)

            await asyncio.gather(*tasks)
            await self.queue.put(None)