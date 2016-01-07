# vdm-ws

## How to run - using Python 3.5

```
pip install Flask
python crawler.py 200 posts.json
python server.py posts.json --debug
```

## TODO

* Implement post_id autoincrement
* Handle date parsing and formatting
* Check cleanup/trimming of parsed content
* Implement other endpoints
* Cleanup argument parsing using getopt module