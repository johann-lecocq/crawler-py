class ArticleCrawler:
    """Represent an ArticleCrawler"""

    def page(self, id):
        """return all article of the page
            id identfiant of the page
        """
        return 200, []

    def article(self, id):
        """return an article identified by id
            id identfiant of the article
        """
        return 200, None

    def random(self):
        """return all article of a random page
        """
        return 200, []

class ParseException(Exception):
    pass
