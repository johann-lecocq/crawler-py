# -*- coding: utf-8 -*-
import re

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
        for article in soup.find_all("article"):
            if article.find("a", href=re.compile(r"subscribe")):
                continue
            a_content = article.find("p", class_=re.compile(r"summary")).find("a")
            id_ = a_content.get("href").replace("/", "")
            texte = a_content.children.__next__().getText()
            article = Article(id_)
            section = Section("anecdote")
            section.add_content(Data("string", texte))
            article.add_section(section)
            reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)


def parse_article(text) -> Section:
    try:
        soup = BeautifulSoup(text, 'html.parser')
        article = soup.find("article")
        p_content = article.find("p", class_=re.compile(r"summary"))
        texte = p_content.getText()
        section = Section("anecdote")
        section.add_content(Data("string", texte))
        return section
    except Exception as e:
        raise ParseException(e)


class ScmbCrawler(ArticleCrawler):
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
        code, data = self.__go(LIEN_PAGE.format(int(id_) + 1), parse)
        return code, data

    def article(self, id_):
        code, data = self.__go(LIEN_ARTICLE.format(id_), parse_article)
        article = Article(id_)
        article.add_section(data)
        return code, article

    def random(self):
        code, data = self.__go(LIEN_ALEATOIRE, parse)
        return code, data
