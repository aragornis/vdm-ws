# vdm-ws

## CLI
```
python crawler.py [200] [posts.json] # Runs crawler
python server.py [posts.json] [--debug] # Starts server
```

## How to run - using Python 3.5

```
pip install python-dateutil
pip install pydblite
pip install Flask
python crawler.py 200 posts.json
python server.py posts.json --debug
```

## TODO

* Cleanup argument parsing using getopt module