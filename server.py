from flask import Flask
server = Flask(__name__)

@server.route("/api/posts")
def hello():
    return "{}"

if __name__ == "__main__":
    app.run()