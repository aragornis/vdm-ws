from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
import json
import sys

server = Flask(__name__)

def load_posts(file):
    with open(file, 'r') as f:
        return json.load(f)

def filter_by_from_date(seq, from_date):
   for el in seq:
       if el['date'] >= from_date: yield el

def filter_by_to_date(seq, to_date):
   for el in seq:
       if el['date'] <= to_date: yield el

def filter_by_author(seq, author):
   for el in seq:
       if el['author'] == author: yield el

@server.route("/api/posts")
def get_all_posts():
    filtered_posts = posts

    fromDate = request.args.get('from', None)
    if fromDate != None:
        filtered_posts = filter_by_from_date(filtered_posts, fromDate)

    toDate = request.args.get('to', None)
    if toDate != None:
        filtered_posts = filter_by_to_date(filtered_posts, toDate) 

    author = request.args.get('author', None)
    if author != None:    
        filtered_posts = filter_by_author(filtered_posts, author)

    result = list(filtered_posts)
    return jsonify(post = result, count = len(result))

@server.route("/api/post/<id>")
def get_post(id):
    post_id = int(id)
    result = next((post for post in posts if post['id'] == post_id), None)    
    return jsonify(post = result) if result != None else abort(404)

if __name__ == "__main__":
     # Parse arguments
    library_file = sys.argv[1] or 'posts.json'
    debug = len(sys.argv) > 2 and sys.argv[2] == '--debug'

    # Load posts database
    posts = load_posts(library_file)
    print("%s posts loaded from %s" % (len(posts), library_file))

    # Start server
    server.run(debug=debug)