# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from re import findall,I,U
from bs4 import BeautifulSoup

from crawlerpy.parser import Parser,ParseException
from crawlerpy.objet import *

class VdmParser(Parser):
    """The implementation of VideDeMerde site parser"""
    def __init__(self):
        pass
    def __recherche_div_page(self,racine):
        principal=None
        divs=racine.find_all("div")
        for div in divs:
            attribut=div.get("class")
            if not (attribut is None) and "infinite-scroll" in attribut:
                principal=div
                break
        if not principal is None:
            return principal

        for div in divs:
            attribut=div.get("id")
            if not (attribut is None) and "content" in attribut:
                principal=div
                break
        divs=principal.find_all("div")
        for div in divs:
            attribut=div.get("class")
            if not (attribut is None) and "col-sm-8" in attribut:
                principal=div
                break
        return principal
    def parse(self,text):
        try:
            reponse=[]
            soup = BeautifulSoup(text, 'html.parser')
            if "VDM :     Aujourd" in soup.find("title").getText():
                article = soup.find("article")
                if article is None :
                    return []
                text = article.find("p")
                if text is None:
                    return []
                l=article.find("a").get("href").replace("/article/","").replace("/","__").replace(".html","")
                section=Section("text")
                section.add_content(Data("string",text.getText()))
                a=Article(l)
                a.add_section(section)
                reponse.append(a)
            else:
                principal=self.__recherche_div_page(soup)
                articles=principal.find_all("article")
                for article in articles:
                    attribut=article.get("class")
                    if attribut is None or "art-panel" not in attribut:
                        continue
                    block=article.find("p")
                    content=block.find("a")
                    if 'http://www.public.fr' in content.get("href") or "http://people.premiere.fr" in content.get("href"):
                        continue
                    text = content.getText().strip()
                    if text[0:11]!="Aujourd'hui" or text[-3:]!="VDM":
                        continue
                    section=Section("text")
                    section.add_content(Data("string",text))
                    l=content.get("href").replace("/article/","").replace("/","__").replace(".html","")
                    a=Article(l)
                    a.add_section(section)
                    reponse.append(a)
            return reponse
        except Exception as e:
            print(e)
            raise ParseException()
