from urllib.request import urlopen

class Fetcher:
    """ Reponsible for downloading content from vdm website. """

    def downloadPage(self, page_index):
        """ Returns the content of vdm's page with index page_index as a string. """
        return urlopen("http://www.viedemerde.fr/?page=%s" % page_index).read().decode('utf-8')