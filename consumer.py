from bs4 import BeautifulSoup
import os
import json
import asyncio

class Consumer:
    def __init__(self, queue):
        self.queue = queue
        self.output = {}

    def cleanURL(self, url, rootURL):
        if url.startswith('/'):
            return rootURL.rstrip('/') + url
        elif url.startswith('#'):
            rootURL = rootURL + '/' if not rootURL.endswith('/') else rootURL
            return rootURL + url
        else:
            return url

    def processItem(self, item):
        parser = BeautifulSoup(item['content'], 'html.parser')
        a_tags = parser.find_all('a')

        if (item['url'] in self.output):
            print(f"{item['url']} already processed, skipping.")
        else:
            urls_all = []
            for tag in a_tags:
                url = tag.get('href')
                if url:
                    url = self.cleanURL(url, item['url'])
                    urls_all.append(url)

            self.output[item['url']] = urls_all

    async def run(self):
        end = False
        while True:
            item = await self.queue.get()
            if (item == None):
                end = True
            else:
                self.processItem(item)
                self.queue.task_done()

            if self.queue.empty() and end:
                break

        with open('output.json', 'w') as f:
            json.dump(self.output, f, indent=4)