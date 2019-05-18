# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from html import unescape

from crawlerpy import ArticleCrawler, ParseException
from crawlerpy.sap import Article, Section, Data
from crawlerpy.util import get

LIEN_ACCUEIL = "http://secouchermoinsbete.fr"
LIEN_ALEATOIRE = "http://secouchermoinsbete.fr/random"
LIEN_PAGE = "http://secouchermoinsbete.fr/?page={0}"
LIEN_ARTICLE = "http://secouchermoinsbete.fr/{0}"


def parse(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        articles = soup.find_all("article")
        for article in articles:
            if "anecdote" not in article.get("class"):
                continue
            header = article.find("header")
            if header is None:  # if one article in the page
                for cl in soup.find_all("section"):
                    if cl.get("id") == "anecdote-item":
                        container_lien = soup.find("section").find("h1")
            else:  # many article in the page
                container_lien = header.find("h1")
            lien = container_lien.find("a").get("href").replace("/", "")
            text = article.find("p").get_text().replace('En savoir plus', "").strip()
            section = Section("anecdote")
            section.add_content(Data("string", text))
            article = Article(lien)
            article.add_section(section)
            reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)


class ScmbCrawler(ArticleCrawler):
    """The implementation of VieDeMerde crawler"""
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
            code = 200
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