# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from bs4 import BeautifulSoup

from crawlerpy.objet import *
from crawlerpy.parser import Parser,ParseException


__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.3"


class ScmbParser(Parser):
	"""The implementation of SeCoucherMoinsBete site parser"""
	def __init__(self):
		pass
	def parse(self,text):
		try:
			reponse=[]
			soup = BeautifulSoup(text, 'html.parser')
			articles=soup.find_all("article")
			for article in articles:
				if "anecdote" not in article.get("class"):
					continue
				header=article.find("header")
				if header is None:# if one article in the page
					for cl in soup.find_all("section"):
						if cl.get("id")=="anecdote-item":
							container_lien=soup.find("section").find("h1")
				else:#many article in the page
					container_lien=header.find("h1")
				lien=container_lien.find("a").get("href").replace("/","")
				text=article.find("p").get_text().replace('En savoir plus',"").strip()
				section=Section("anecdote")
				section.add_content(Data("string",text))
				article=Article(lien)
				article.add_section(section)
				reponse.append(article)
			return reponse
		except Exception as e:
			print(e)
			raise ParseException()
