from urllib.request import urlopen
from posts import repository
from crawler.parser import Parser
import re
import sys

def download_page(page_index):
    return urlopen("http://www.viedemerde.fr/?page=%s" % page_index).read().decode('utf-8')

def crawl(nb_requested):
    results = []
    current_page_index = 0
    parser = Parser()

    while len(results) < nb_requested:
        current_page = download_page(current_page_index)
        new_results = parser.parse(current_page)

        if len(new_results) == 0:
            raise StopIteration("Empty page found, aborting crawling")

        results += new_results
        current_page_index += 1

    del results[nb_requested:]
    return results

if __name__ == "__main__":
    # Parse arguments
    nb_requested_posts = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    library_file = sys.argv[2] if len(sys.argv) > 2 else "posts.pdl"

    # Start crawling
    posts = crawl(nb_requested_posts)
    repository = repository.Posts(library_file, True)

    # Persist posts
    for post in posts:
        repository.addPost(post)

    print("%s posts have been parsed and saved to %s" % (repository.getPostsCount(), library_file))