# -*- coding: utf-8 -*-

__author__ = "Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from html import unescape

from crawlerpy import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawlerpy.parser import ParseException
from crawlerpy.parser.dtc import DtcParser


LIEN_ACCUEIL = "http://danstonchat.com/latest.html"
LIEN_ALEATOIRE = "http://danstonchat.com/random.html"
LIEN_PAGE = "http://danstonchat.com/latest/{}.html"
LIEN_ARTICLE = "http://danstonchat.com/{}.html"

class DtcCrawler(ArticleCrawler):
	"""The implementation of DansTonChat crawler"""
	def __init__(self):
		super().__init__(DtcParser(), HttpCommunicator())
	def __go(self, lien):
		reponse = self.aspirateur.get(lien)
		if reponse["code"] == 200:
			text = unescape(reponse["data"])
			try:
				data = self.parser.parse(text)
			except ParseException:
				print(e)
				return(521,[])
			code = 200
		else:
			code = reponse["code"]
			data = []
		return (code, data)
	def page(self, id_):
		global LIEN_PAGE
		(code, data) = self.__go(LIEN_PAGE.format(int(id_)+1))
		return ResponseCrawler(code,data)
	def article(self, id_):
		global LIEN_ARTICLE
		(code, data) = self.__go(LIEN_ARTICLE.format(id_))
		return ResponseCrawler(code,data)
	def page_random(self):
		global LIEN_ALEATOIRE
		(code, data) = self.__go(LIEN_ALEATOIRE)
		return ResponseCrawler(code,data)
	def article_random(self):
		global LIEN_ALEATOIRE
		(code, data) = self.__go(LIEN_ALEATOIRE)
		if len(data)>0:
			data=[data[0]]
		return ResponseCrawler(code,data)
