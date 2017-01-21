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
    def parse(self,text):
        print("je passe dans le parser")
        try:
            reponse=[]
            soup = BeautifulSoup(text, 'html.parser')
            articles=soup.find_all("article")
            print(len(articles))
            for article in articles:
                attribut=article.get("class")
                if attribut is None or "art-panel" not in attribut:
                    continue
                block=article.find("p")
                content=block.find("a")
                print(content.get("href"))
                print(content.getText())
                if 'http://www.public.fr' in content.get("href") or "http://people.premiere.fr" in content.get("href"):
                    continue
                section=Section("text")
                section.add_content(Data("string",content.getText()))
                l=content.get("href").replace("/article/","").replace("/","__").replace(".html","")
                a=Article(l)
                a.add_section(section)
                reponse.append(a)
            print(reponse,len(reponse))
            return reponse
        except Exception as e:
            print(e)
            raise ParseException()
