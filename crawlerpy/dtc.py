# -*- coding: utf-8 -*-
import re
from html import unescape

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from crawlerpy import ArticleCrawler, ParseException
from crawlerpy.sap import Article, Section, Data
from crawlerpy.util import get

LIEN_ALEATOIRE = "https://danstonchat.com/random"
LIEN_PAGE = "https://danstonchat.com/?query-8-page={0}"
LIEN_ARTICLE = "https://danstonchat.com/quote/{0}.html"


def parse_content(element) -> Section:
    div_content = element.find("div", class_=re.compile(r"^entry-content"))
    section = Section("quote")
    t = ""
    for e in div_content.find("p").children:
        if e.name == "br":
            section.add_content(Data("string", t))
            t = ""
        elif e.name == "span":
            for d in e.contents:
                if type(d) == Tag:
                    t = "<" + d.name + "> "
                    break
            else:
                t = "".join(e.find_all(text=True, recursive=False)).strip() + " "
        elif type(e) == NavigableString:
            t += e.string.strip()
    section.add_content(Data("string", t))
    return section


def parse_title_content(article):
    html_titre = article.find("h2").find("a")
    identifiant = html_titre.attrs["href"].replace("https://danstonchat.com/quote/", "").replace(".html", "")
    section_quote = parse_content(article)
    article = Article(identifiant)
    article.add_section(section_quote)
    return article


def parse_page(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        for article in soup.find_all("article"):
            if article.find_all("figure") or article.find("h2") is None:
                continue
            reponse.append(parse_title_content(article))
        return reponse
    except Exception as e:
        raise ParseException(e)


def parse_random(text):
    try:
        reponse = []
        soup = BeautifulSoup(text, 'html.parser')
        div_content = soup.find("main").find("div", class_=re.compile(r"^entry-content"))
        for article in div_content.find_all("li", class_=re.compile(r"post-\d")):
            reponse.append(parse_title_content(article))
        return reponse
    except Exception as e:
        raise ParseException(e)


def parse_article(text, id_):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        div_main = soup.find("main")
        title = div_main.find("h1").get_text().strip()
        content = parse_content(div_main)
        article = Article(id_)
        article.add_section(content)
        return article
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
            return 200, parse_random(data)
        except ParseException:
            return 521, []
