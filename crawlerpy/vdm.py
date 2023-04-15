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
        principale_div = soup.find("div",attrs={"class":"jscroll-inner"})
        for div in principale_div.find_all("article"):
            for a in div.find_all("a"):
                cl = a.get("class")
                if cl and "block" in cl:
                    id_= a.get("href").replace("/article/", "").replace(".html", "")
                    citation = "".join(a.find_all(text=True, recursive=False)).strip()
                    break
            article = Article(id_)
            section = Section("citation")
            section.add_content(Data("string",citation))
            article.add_section(section)
            reponse.append(article)
        return reponse
    except Exception as e:
        raise ParseException(e)

def parse_article(text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        for principale_div in soup.find_all("div"):
            cl = principale_div.get("class")
            if not (cl and "w-full" in cl and "lg:w-2/3" in cl):
                continue
            div = principale_div.find("article")
            for a in div.find_all("a"):
                cl = a.get("class")
                if cl and "block" in cl:
                    id_= a.get("href").replace("/article/", "").replace(".html", "")
                    citation = "".join(a.find_all(text=True, recursive=False)).strip()
                    break
            section = Section("citation")
            section.add_content(Data("string",citation))
            return section
    except Exception as e:
        raise ParseException(e)

def parse_random(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        for principale_div in soup.find_all("div", class_=re.compile("^w-full lg")):
            for div in principale_div.find_all("article"):
                for a in div.find_all("a"):
                    cl = a.get("class")
                    if cl and "block" in cl:
                        id_= a.get("href").replace("/article/", "").replace(".html", "")
                        citation = "".join(a.find_all(text=True, recursive=False)).strip()
                        break
                article = Article(id_)
                section = Section("citation")
                section.add_content(Data("string",citation))
                article.add_section(section)
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
            code = 200
        return code, []

    def page(self, id_):
        (code, data) = self.__go(LIEN_PAGE.format(int(id_)+1), parse_page)
        return code, data

    def article(self, id_):
        (code, section) = self.__go(LIEN_ARTICLE.format(id_), parse_article)
        article = Article(id_)
        article.add_section(section)
        return code, article

    def random(self):
        (code, data) = self.__go(LIEN_ALEATOIRE,parse_random)
        return code, data