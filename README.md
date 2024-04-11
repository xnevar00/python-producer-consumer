# Python producer-consumer

Producer fetches HTML content from given URLs and hands it to consumer via queue. Consumer processes the content and extracts all hyperlinks from it and saves it as a JSON. App can be run either in local environment or as a docker container.

## Dependencies
- installed python>=3.10
- docker, docker-compose (in case of containerization)
## Installing dependencies
``` bash
pip3 install -r requirements.txt
```

## Run tests
```bash
pytest consumer.py
```

## How to run
### Input file
create a .txt file with URLs each on single line, e.g.:

```
https://www.google.com 
https://www.vut.cz
https://www.fit.vut.cz
https://seznam.cz
```
### Run
```
python3 app.py [file]
```

## Containerization
### Input file
create a `input.txt` file with URLs in app directory

### Run container
```bash
docker-compose up -d
```
output should be in `output` folder