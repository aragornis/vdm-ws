from urllib.request import urlopen

class Fetcher:
    def downloadPage(self, page_index):
        return urlopen("http://www.viedemerde.fr/?page=%s" % page_index).read().decode('utf-8')