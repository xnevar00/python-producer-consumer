from bs4 import BeautifulSoup
import os
import json
import asyncio

class Consumer:
    """
    Class that processes json data from Producer and gets all hyperlinks from
    HTML content

    Attributes: 
        queue (asyncio.Queue): queue for the data jsons to be put to
        output (dict): output content containing all links for all urls
    """

    def __init__(self, queue: asyncio.Queue):
        self.queue = queue
        self.output = {}

    def cleanURL(self, url: str, rootURL: str) -> str :
        """
        In case the given hyperlink is for example '/subpage' or '#',
        the root url is added before that so the url is valid

        Parameters:
            url (str): hyperlink from HTML content
            rootURL (str): root url of the web it was fetched from

        Returns:
            url (str): whole valid url
        """
        if url.startswith('/'):
            return rootURL.rstrip('/') + url
        elif url.startswith('#'):
            rootURL = rootURL + '/' if not rootURL.endswith('/') else rootURL
            return rootURL + url
        elif not url.startswith("http"):
            url = None
        else:
            return url

    def processItem(self, item: dict) -> None :
        """
        Processes all urls from HTML content and adds them into the output
        dict as an array for every URL given in the url file

        Parameters:
            item (dict): contains name of the URL and its HTML content
        """
        parser = BeautifulSoup(item['content'], 'html.parser')
        a_tags = parser.find_all('a')

        if (item['url'] in self.output): # dont process same url multiple times
            print(f"{item['url']} already processed, skipping.")
        else:
            urls_all = []
            for tag in a_tags:
                url = tag.get('href') # get hyperlink
                if url:
                    url = self.cleanURL(url, item['url'])
                    if url is not None:
                        urls_all.append(url)

            self.output[item['url']] = urls_all

    async def run(self) -> None :
        """
        Gets items from queue and calls their processing
        """
        end = False
        while True:
            item = await self.queue.get()
            if (item == None):
                end = True
            else:
                self.processItem(item)
                self.queue.task_done()

            if self.queue.empty() and end: # there is nothing to be processed
                break
        
        output_filename = "./data/output.json"
        os.makedirs("data", exist_ok=True)
        with open(output_filename, 'w') as f:
            json.dump(self.output, f, indent=4)

def test_process_item():
    consumer = Consumer(None)
    item = {'url': 'https://www.example.com', 'content': '<a href="https://www.example.com/test"/>'}
    consumer.processItem(item)

    correct_output = ['https://www.example.com/test']

    assert consumer.output[item['url']] == correct_output

def test_process_item_invalid_href():
    consumer = Consumer(None)
    item = {'url': 'https://www.example.com', 'content': '<a href="test">'}
    consumer.processItem(item)

    correct_output = []

    assert consumer.output[item['url']] == correct_output

def test_clean_URL():
    consumer = Consumer(None)
    output = consumer.cleanURL('/a', 'https://www.example.com')

    correct_output = 'https://www.example.com/a'
    assert output == correct_output

def test_clean_URL_invalid_href():
    consumer = Consumer(None)
    output = consumer.cleanURL('test', 'https://www.example.com')

    correct_output = None
    assert output == correct_output