# -*- coding: utf-8 -*-
from html import unescape
from re import findall, I, U, DOTALL

from crawlerpy import ArticleCrawler, ParseException
from crawlerpy.sap import Article, Section, Data
from crawlerpy.util import get

LIEN_ACCUEIL = "http://danstonchat.com/latest.html"
LIEN_ALEATOIRE = "http://danstonchat.com/random.html"
LIEN_PAGE = "http://danstonchat.com/latest/{0}.html"
LIEN_ARTICLE = "http://danstonchat.com/{0}.html"

flags = I | U | DOTALL

def parse(text):
    try:
        reponse = []
        for ident, quote in findall(r'<a href="https://danstonchat\.com/(\d+)\.html">(.*?)</a>', text, flags):
            quote = quote.strip() + "<br />"
            article = Article(ident)
            section = Section("quote")
            elements = findall(r'<span class="decoration" style="background-color: RGB\(\d{3},\d{3},\d{3}\);">(.*?)</span>(.*?)<br />', quote, flags)
            for pseudo, text in elements:
                section.add_content(Data("string", pseudo.strip() + " " + text.strip()))
            if elements:
                article.add_section(section)
                reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)


class DtcCrawler(ArticleCrawler):
    """The implementation of DansTonChat crawler"""
    def __init__(self):
        ArticleCrawler.__init__(self)

    def __go(self, lien):
        code, text = get(lien)
        if code == 200:
            text = unescape(text)
            try:
                return 200, parse(text)
            except ParseException:
                return 521, []
        return code, []

    def page(self, id_):
        code, data = self.__go(LIEN_PAGE.format(int(id_) + 1))
        return code, data

    def article(self, id_):
        code, data = self.__go(LIEN_ARTICLE.format(id_))
        return code, data[0]

    def random(self):
        code, data = self.__go(LIEN_ALEATOIRE)
        return code, data
