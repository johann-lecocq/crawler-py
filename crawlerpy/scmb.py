# -*- coding: utf-8 -*-

__author__ = "Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from html import unescape

from crawlerpy import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawlerpy.parser import ParseException
from crawlerpy.parser.scmb import ScmbParser

LIEN_ACCUEIL = "http://secouchermoinsbete.fr"
LIEN_ALEATOIRE = "http://secouchermoinsbete.fr/random"
LIEN_PAGE = "http://secouchermoinsbete.fr/?page={0}"
LIEN_ARTICLE = "http://secouchermoinsbete.fr/{0}"


class ScmbCrawler(ArticleCrawler):
    """The implementation of VieDeMerde crawler"""

    def __init__(self):
        super().__init__(ScmbParser(), HttpCommunicator())

    def __go(self, lien):
        reponse = self.aspirateur.get(lien)
        if reponse["code"] == 200:
            text = unescape(reponse["data"])
            try:
                data = self.parser.parse(text)
            except ParseException:
                return 521, []
            code = 200
        else:
            code = reponse["code"]
            data = []
        return code, data

    def page(self, id_):
        code, data = self.__go(LIEN_PAGE.format(id_ + 1))
        return ResponseCrawler(code, data)

    def article(self, id_):
        code, data = self.__go(LIEN_ARTICLE.format(id_))
        return ResponseCrawler(code, data)

    def page_random(self):
        code, data = self.__go(LIEN_ALEATOIRE)
        return ResponseCrawler(code, data)

    def article_random(self):
        code, data = self.__go(LIEN_ALEATOIRE)
        if len(data) > 0:
            data = [data[0]]
        return ResponseCrawler(code, data)
