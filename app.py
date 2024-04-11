import argparse
from consumer import Consumer
from producer import Producer
import asyncio
import os


def getUrlFile() -> str:

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('File', type=str, help='File containing urls, each on a single line.')
    args = parser.parse_args()
    return args.File

async def run(producer: Producer, consumer: Consumer) -> None:

    await asyncio.gather(producer.run(), consumer.run())

if __name__ == "__main__":
    file = getUrlFile()
    
    if not os.path.exists(file):
        print(f"File {file} does not exist.")
        exit()

    queue = asyncio.Queue(maxsize=50)
    producer = Producer(file, queue)
    consumer = Consumer(queue)

    asyncio.run(run(producer, consumer))
