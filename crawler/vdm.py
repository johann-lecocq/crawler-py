# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.0"

from html import unescape

from crawler import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawler.parser.vdm import VdmParser


LIEN_ACCUEIL="http://m.viedemerde.fr"
LIEN_ALEATOIRE="http://m.viedemerde.fr/aleatoire"
LIEN_PAGE="http://m.viedemerde.fr/?page=%d"
LIEN_ARTICLE="http://m.viedemerde.fr/%d"

class VdmCrawler(ArticleCrawler):
	"""The implementation of VieDeMerde crawler"""
	def __init__(self):
		super().__init__(VdmParser(),HttpCommunicator())
	def __go(self,lien):
		reponse=self.aspirateur.get(lien)
		if reponse["code"]==200:
			text=unescape(reponse["data"]).replace("&quot;","'")
			data=self.parser.parse(text)
			code=200
		else:
			code=reponse["code"]
			data=[]
		return ResponseCrawler(code,data)
		return self.parser.parse(text)
	def page(self,id_):
		global LIEN_PAGE
		return self.__go(LIEN_PAGE % (id_))
	def article(self,id_):
		global LIEN_ARTICLE
		return self.__go(LIEN_ARTICLE % id_)
	def page_random(self):
		global LIEN_ALEATOIRE
		return self.__go(LIEN_ALEATOIRE)
	def article_random(self):
		global LIEN_ALEATOIRE
		return self.__go(LIEN_ALEATOIRE)