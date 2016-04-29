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
		try:
			reponse=[]
			soup = BeautifulSoup(text, 'html.parser')
			articles=soup.find_all("div")
			for article in articles:
				attribut=article.get("class")
				if attribut is None or "article" not in attribut:
					continue
				article=article.find("a")
				attribut=article.get("class")
				if  attribut is None or "fmllink" not in attribut:
					continue
				section=Section("text")
				section.add_content(Data("string",article.getText()))
				article=Article(article.get("href")[1::].replace("/","_"))
				article.add_section(section)
				reponse.append(article)
			return reponse
		except Exception as e:
			print(e)
			raise ParseException()
