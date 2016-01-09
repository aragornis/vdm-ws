from urllib.request import urlopen
from posts.repository import Posts
from crawler.parser import Parser
from crawler.fetcher import Fetcher
from crawler.crawler import Crawler
import sys

if __name__ == "__main__":
    # Parse arguments
    nb_requested_posts = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    library_file = sys.argv[2] if len(sys.argv) > 2 else "posts.pdl"

    # Crawl
    crawler = Crawler(Fetcher(), Parser())
    posts = crawler.crawl(nb_requested_posts)

    # Persist crawled posts
    repository = Posts(library_file, True)
    for post in posts:
        repository.addPost(post)

    print("%s posts have been parsed and saved to %s" % (repository.getPostsCount(), library_file))