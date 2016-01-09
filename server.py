from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from posts.repository import *
import json
import sys
from dateutil import parser
from dateutil import tz

server = Flask(__name__)

@server.route("/api/posts")
def get_all_posts():
    fromDate = tryParseDate(request.args.get('from', None))
    toDate = tryParseDate(request.args.get('to', None))
    author = request.args.get('author', None)

    result = [p.toDisplayableDict() for p in repository.getPosts(fromDate, toDate, author)]
    return jsonify(post = result, count = len(result))

def tryParseDate(rawDate):
    if rawDate is not None:
        date = parser.parse(rawDate, dayfirst = True, default = None)
        if date is not None:
            return date.replace(tzinfo= tz.gettz('Europe/Paris'))
    return None

@server.route("/api/post/<id>")
def get_post(id):
    post_id = int(id)
    result = repository.getPost(post_id)
    return jsonify(post = result.toDisplayableDict()) if result != None else abort(404)

if __name__ == "__main__":
     # Parse arguments
    library_file = sys.argv[1] or 'posts.pdl'
    debug = len(sys.argv) > 2 and sys.argv[2] == '--debug'

    # Load posts database
    repository = Posts(library_file, False)
    print("%s posts loaded from %s" % (repository.getPostsCount(), library_file))

    # Start server
    server.run(debug=debug)