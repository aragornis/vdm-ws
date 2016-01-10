# vdm-ws

## CLI
```
python crawler.py [nb_posts] [db_file] # Runs crawler
python server.py [db_file] [--debug] # Starts server
```

## How to run tests

```
python -m unittest discover
```

## How to run - using Python 3.5

```
pip install -r requirements.txt
python crawler.py 200 posts.pdl
python server.py posts.pdl --debug

curl http://localhost:5000/api/posts
curl http://localhost:5000/api/posts?from=2016-01-10
curl http://localhost:5000/api/post/3
```

## TODO

* Cleanup argument parsing using getopt module