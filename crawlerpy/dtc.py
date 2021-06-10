# -*- coding: utf-8 -*-
from html import unescape
#from re import findall, I, U, DOTALL
from bs4 import BeautifulSoup
from bs4.element import NavigableString

from crawlerpy import ArticleCrawler, ParseException
from crawlerpy.sap import Article, Section, Data
from crawlerpy.util import get

LIEN_ACCUEIL = "http://danstonchat.com/latest.html"
LIEN_ALEATOIRE = "http://danstonchat.com/random.html"
LIEN_PAGE = "http://danstonchat.com/latest/{0}.html"
LIEN_ARTICLE = "http://danstonchat.com/{0}.html"


def parse_contenu(div):
    t = div.find("h3")
    titre=""
    if t:
        titre = "".join(t.find("a").find_all(text=True, recursive=False)).strip()
    identifiant = "".join(div.get("class")).replace("item","").strip()
    article = Article(identifiant)
    section = Section("quote")
    t=""
    for e in div.find("div",attrs={"class":"item-content"}).find("a").children:
        if e.name=="span":
            t="".join(e.find_all(text=True, recursive=False)).strip()
        elif type(e)== NavigableString:
            section.add_content(Data("string", t+e.string.strip()))
    article.add_section(section)
    return article

def parse_page(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        d = soup.find("div",attrs={"class":"items"})
        for div in d.find_all("div", recursive=False):
            reponse.append(parse_contenu(div))
        return reponse
    except Exception as e:
        raise ParseException(e)

def parse_article(text, id_):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        return parse_contenu(soup.find("div",attrs={"id":id_}))
    except Exception as e:
        raise ParseException(e)

class DtcCrawler(ArticleCrawler):
    """The implementation of DansTonChat crawler"""
    def __init__(self):
        ArticleCrawler.__init__(self)

    def get_text(self, lien):
        code, text = get(lien)
        if code == 200:
            text = unescape(text)
        return code, text

    def page(self, id_):
        code, data = self.get_text(LIEN_PAGE.format(int(id_) + 1))
        if code != 200:
            return code, []
        try:
            return 200, parse_page(data)
        except ParseException:
            return 521, []

    def article(self, id_):
        code, data = self.get_text(LIEN_ARTICLE.format(id_))
        if code != 200:
            return code, []
        try:
            return 200, parse_article(data, id_)
        except ParseException:
            return 521, []

    def random(self):
        code, data = self.get_text(LIEN_ALEATOIRE)
        if code != 200:
            return code, []
        try:
            return 200, parse_page(data)
        except ParseException:
            return 521, []
