from urllib.request import urlopen
from html.parser import HTMLParser
from posts.repository import *
import re
import sys

regex = re.compile('<div class="post article" id="\d+"><p>(.*?)<\/p><div class="date"><div class="left_part">.*?<p>Le ([^-]*?) - .*? - par (.*?) (\(<a.*?<\/a>\))?<\/p><\/div>', re.MULTILINE)

def download_page(page_index):
    return urlopen("http://www.viedemerde.fr/?page=%s" % page_index).read().decode('utf-8')

def create_post_from_match(match):
    parser = HTMLParser()
    return Post(match[2], re.sub('<[^<]+?>', '', parser.unescape(match[0])), match[1])

def parse_page(page):
    return [create_post_from_match(m) for m in regex.findall(page)]

def crawl(nb_requested):
    results = []
    current_page_index = 0

    while len(results) < nb_requested:
        current_page = download_page(current_page_index)
        new_results = parse_page(current_page)

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
    repository = Posts(library_file, True)

    # Persist posts
    for post in posts:
        repository.addPost(post)

    print("%s posts have been parsed and saved to %s" % (repository.getPostsCount(), library_file))