# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from html import unescape

from crawlerpy import ArticleCrawler, ParseException
from crawlerpy.sap import Article, Section, Data
from crawlerpy.util import get

LIEN_ACCUEIL = "https://www.viedemerde.fr"
LIEN_ALEATOIRE = "https://www.viedemerde.fr/aleatoire"
LIEN_PAGE = "https://www.viedemerde.fr/?page={}"
LIEN_ARTICLE = "https://www.viedemerde.fr/article/{}.html"


def parse_page(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        div_principale = soup.find("div", class_=re.compile("^w-full lg"))
        for article_html in div_principale.find_all("article"):
            citation = None
            for a in article_html.find_all("a"):
                cl = a.get("class")
                if cl and "block" in cl:
                    id_ = a.get("href").replace("/article/", "").replace(".html", "")
                    citation = "".join(a.find_all(text=True, recursive=False)).strip()
                    break
            article = Article(id_)
            section_citation = Section("citation")
            section_citation.add_content(Data("string", citation))
            article.add_section(section_citation)
            reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)


def parse_article(text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        div_principale = soup.find("div", class_=re.compile("^w-full lg"))
        article_html = div_principale.find("article")
        citation = None
        id_ = None
        for span in article_html.find_all("span"):
            cl = span.get("class")
            if cl and "block" in cl:
                citation = span.getText().strip()

        for a in article_html.find_all("a"):
            cl = a.get("class")
            if cl is None:
                id_ = a.get("href").replace("/article/", "").replace(".html", "")
        article = Article(id_)
        section_citation = Section("citation")
        section_citation.add_content(Data("string", citation))
        article.add_section(section_citation)
        return article
    except Exception as e:
        raise ParseException(e)


def parse_random(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        div_principale = soup.find("div", class_=re.compile("^w-full lg"))
        for article_html in div_principale.find_all("article"):
            citation = None
            for a in article_html.find_all("a"):
                cl = a.get("class")
                if cl and "block" in cl:
                    id_ = a.get("href").replace("/article/", "").replace(".html", "")
                    citation = "".join(a.find_all(text=True, recursive=False)).strip()
                    break
            article = Article(id_)
            section_citation = Section("citation")
            section_citation.add_content(Data("string", citation))
            article.add_section(section_citation)
            reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)


class VdmCrawler(ArticleCrawler):
    """The implementation of VieDeMerde crawler"""

    def __init__(self):
        ArticleCrawler.__init__(self)

    def __go(self, lien, parse_function):
        code, text = get(lien)
        if code == 200:
            text = unescape(text)
            try:
                return 200, parse_function(text)
            except ParseException:
                return 521, []
        return code, []

    def page(self, id_):
        code, data = self.__go(LIEN_PAGE.format(int(id_) + 1), parse_page)
        return code, data

    def article(self, id_):
        code, article = self.__go(LIEN_ARTICLE.format(id_), parse_article)
        return code, article

    def random(self):
        code, data = self.__go(LIEN_ALEATOIRE, parse_random)
        return code, data
