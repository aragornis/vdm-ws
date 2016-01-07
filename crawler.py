from urllib.request import urlopen
from html.parser import HTMLParser
import re
import json
import sys

library_file = 'posts.json'
regex = re.compile('<div class="post article" id="\d+"><p>(.*?)<\/p><div class="date"><div class="left_part">.*?<p>Le ([^-]*?) - .*? - par (.*?)(\(<a.*?<\/a>\))?<\/p><\/div>', re.MULTILINE)

def download_page(page_index):
    return urlopen("http://www.viedemerde.fr/?page=%s" % page_index).read().decode('utf-8')

def create_post_from_match(match):
    parser = HTMLParser()
    return {'id': 0, 'content': re.sub('<[^<]+?>', '', parser.unescape(match[0])), 'date': match[1], 'author': match[2]}

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
    nb_requested_posts = int(sys.argv[1])

    # Start crawling
    content = crawl(nb_requested_posts)

    # Save content to a raw json file
    with open(library_file, 'w') as f:
        f.truncate()
        json.dump(content, f, ensure_ascii=False)

    print("%s posts have been parsed and saved to %s" % (len(content), library_file))