import argparse
from consumer import Consumer
from producer import Producer
import asyncio
import os

def getUrlFile() -> str:
    """
    Gets the name of the file containing urls. 
    
    Returns:
        string: name of file containing urls
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('File', type=str, help='File containing urls, each on a single line.')
    args = parser.parse_args()
    return args.File

async def run(producer: Producer, consumer: Consumer) -> None:
    """
    Launches both producers and consumers, creates a queue with maximum
    of 50 items

    Parameters:
        producer (Producer): instance of Producer class that fetches data
        consumer (Consumer): instance of Consumer class that processes data from Producer
    """
    await asyncio.gather(producer.run(), consumer.run())

if __name__ == "__main__":
    file = getUrlFile()
    
    if not os.path.exists(file):
        print(f"File {file} does not exist.")
        exit()

    #initialization of all instances needed 
    queue = asyncio.Queue(maxsize=50)
    producer = Producer(file, queue)
    consumer = Consumer(queue)

    asyncio.run(run(producer, consumer))
