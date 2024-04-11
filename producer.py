import asyncio
import aiohttp

class Producer:
    """
    Class that fetches URLs and puts them into a queue as a json

    Attributes: 
        url_file (str): name of the file containing urls
        queue (asyncio.Queue): queue for the data jsons to be put to
    """
    def __init__(self, url_file: str, queue: asyncio.Queue):
        self.url_file = url_file
        self.queue = queue

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> None:
        """
        Fetches data from given url and if the queue is full, it removes an
        oldest item. Then it puts the item to the queue

        Parameters:
            session (aiohttp.CLientSession): an asynchronous HTTP session used for
                                             making HTTP requests 
            url (str): the URL from which to fetch HTML content
        """
        if (url):
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    item = {'url' : url,
                            'content': html}
                    
                    if self.queue.full():
                        await self.queue.get() # remove oldest item from queue
                        print(f"Removed oldest item: {url}")
                    await self.queue.put(item) # put new item into queue

            except Exception as e:
                print(f"Error occured while fetching {url}: {str(e)}",)

    async def run(self) -> None:
        """
        Prepares task for each url and then launches the fetching.
        If all the urls are processed, it will put None into the 
        queue as a sign for consumer to end after processing the
        rest of the items
        """
        async with aiohttp.ClientSession() as session:
            with open(self.url_file, 'r') as file:
                urls = file.readlines()

            tasks = []

            for url in urls:
                url = url.strip()
                task = asyncio.create_task(self.fetch(session, url))
                tasks.append(task)

            await asyncio.gather(*tasks)
            await self.queue.put(None) # end of putting items into the queue -> end