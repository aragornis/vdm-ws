class Crawler:
    def __init__(self, fetcher, parser):
        self.__fetcher = fetcher
        self.__parser = parser

    def crawl(self, nb_requested_posts):
        """ Crawl as much pages as needed to return a list of nb_requested_posts Post objects.
            Raise in case of network issue or when an empty page is found so as to avoid infinite loop
        """
        results = []
        current_page_index = 0

        while len(results) < nb_requested_posts:
            current_page = self.__fetcher.downloadPage(current_page_index)
            new_results = self.__parser.parse(current_page)

            if len(new_results) == 0:
                raise StopIteration("Empty page found, aborting crawling") # Make sure we don't loop forever

            results += new_results
            current_page_index += 1

        # Truncate to return exactly the expected number of posts
        del results[nb_requested_posts:]
        return results