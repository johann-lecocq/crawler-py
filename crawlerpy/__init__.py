# -*- coding: utf-8 -*-

__author__ = "Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

import requests


class Communicator:
    """interface of a Communicator"""

    def get(self, lien):
        """return a dict
        response code(required)->integer
        data(required)"""
        pass


class HttpCommunicator(Communicator):
    """Implementation of Communicator for HTTP"""

    def __init__(self):
        pass

    def get(self, lien):
        text = ""
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }
        reponse = requests.get(lien, headers=headers)

        if reponse.status_code == 200:
            return {"code": 200, "data": reponse.text}

        return {"code": reponse.status_code, "data": ""}


class ArticleCrawler:
    """Represent an ArticleCrawler"""

    def __init__(self, parser, aspirateur):
        self.parser = parser
        self.aspirateur = aspirateur

    def page(self, id_):
        """return ResponseCrawler all article of the page
            id_ identfiant of the page
        """
        pass

    def article(self, id_):
        """return ResponseCrawler article identified by id_
            id_ identfiant of the article
        """
        pass

    def page_random(self):
        """return ResponseCrawler all article of a random page
            id_ identfiant of the article
        """
        pass

    def article_random(self):
        """return ResponseCrawler  a random article
            id_ identfiant of the article
        """
        pass


class ResponseCrawler:
    """ It's an object return by a crawler
        code-> 0 if OK else 1 to NOT OK"""

    def __init__(self, code, data):
        self.code = code
        self.data = data
