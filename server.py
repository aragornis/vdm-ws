from flask import Flask
from flask import jsonify
import json
import sys

server = Flask(__name__)

@server.route("/api/posts")
def get_all_posts():
    return jsonify(post = posts, count = len(posts))

if __name__ == "__main__":
     # Parse arguments
    library_file = sys.argv[1] or 'posts.json'
    debug = len(sys.argv) > 2 and sys.argv[2] == '--debug'

    # Load posts database
    with open(library_file, 'r') as f:
        posts = json.load(f)
        print("%s posts loaded from %s" % (len(posts), library_file))

    # Start server
    server.run(debug=debug)