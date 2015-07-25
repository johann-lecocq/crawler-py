# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.0"

from html import unescape

from crawler import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawler.parser.dtc import DtcParser


LIEN_ACCUEIL="http://danstonchat.com/latest.html"
LIEN_ALEATOIRE="http://danstonchat.com/random.html"
LIEN_PAGE="http://danstonchat.com/latest/%d.html"
LIEN_ARTICLE="http://danstonchat.com/%d.html"

class DtcCrawler(ArticleCrawler):
	"""The implementation of DansTonChat crawler"""
	def __init__(self):
		super().__init__(DtcParser(),HttpCommunicator())
	def __go(self,lien):
		reponse=self.aspirateur.get(lien)
		if reponse["code"]==200:
			text=unescape(reponse["data"])
			data=self.parser.parse(text)
			code=200
		else:
			code=reponse["code"]
			data=[]
		return ResponseCrawler(code,data)
	def page(self,id_):
		global LIEN_PAGE
		return self.__go(LIEN_PAGE % id_)
	def article(self,id_):
		global LIEN_ARTICLE
		return self.__go(LIEN_ARTICLE % id_)
	def page_random(self):
		global LIEN_ALEATOIRE
		return self.__go(LIEN_ALEATOIRE)
	def article_random(self):
		global LIEN_ALEATOIRE
		return self.__go(LIEN_ALEATOIRE)