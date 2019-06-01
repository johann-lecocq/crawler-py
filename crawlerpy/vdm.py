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
LIEN_ARTICLE = "https://www.viedemerde.fr/search/{}"

vdm_id = r'(\d+)\.html$'

def parse_page(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        principale_div = soup.find("div",attrs={"class":"jscroll-inner"})
        for div in principale_div.find_all("div", attrs={"class":"article-contents"}):
            if div.find("iframe"):
                continue
            a = div.find("a")
            id_= a.get("href").replace("/article/", "").replace("/", "__").replace(".html", "")
            if id_.startswith("http") or a.find("img"):
                continue
            article = Article(re.search(vdm_id, a.get("href")).group(1))
            title = a.find("h2",attrs={"class":"classic-title"})
            section = Section("citation")
            if title:
                citation = "".join(a.find_all(text=True, recursive=False)).strip()
                section.add_content(Data("string",citation))
            else:
                section.add_content(Data("string",a.get_text().strip()))
            article.add_section(section)
            reponse.append(article)
        return reponse
    except Exception as e:
        print(e)
        raise ParseException(e)

def parse_article(text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        a = soup.find("a", attrs={"class":"article-link"})

        title = a.find("h2",attrs={"class":"classic-title"})
        section = Section("citation")
        if title:
            citation = "".join(a.find_all(text=True, recursive=False)).strip()
            section.add_content(Data("string",citation))
        else:
            section.add_content(Data("string",a.get_text().strip()))
        
        return section
    except Exception as e:
        raise ParseException(e)

def parse_random(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        principale_div = soup.find("div",attrs={"id":"content"}).find("div",attrs={"class":"col-sm-8"})
        for div in principale_div.find_all("div", attrs={"class":"article-contents"}):
            if div.find("iframe"):
                continue
            a = div.find("a")
            id_= re.search(vdm_id, a.get("href")).group(1)
            if id_.startswith("http") or a.find("img") or a.find("iframe"):
                continue
            article = Article(id_)
            citation = "".join(a.find_all(text=True, recursive=False)).strip()
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
        print(LIEN_PAGE.format(int(id_)+1))
        (code, data) = self.__go(LIEN_PAGE.format(int(id_)+1), parse_page)
        return code, data

    def article(self, id_):
        print(LIEN_ARTICLE.format(id_.replace("__", "/")))
        (code, section) = self.__go(LIEN_ARTICLE.format(id_.replace("__", "/")), parse_article)
        article = Article(id_)
        article.add_section(section)
        return code, article

    def random(self):
        print(LIEN_ALEATOIRE)
        (code, data) = self.__go(LIEN_ALEATOIRE,parse_random)
        return code, data