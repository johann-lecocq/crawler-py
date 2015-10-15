# -*- coding: utf-8 -*-

__author__ = "Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.1"

from html import unescape

from crawlerpy import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawlerpy.parser.vdm import VdmParser


LIEN_ACCUEIL = "http://m.viedemerde.fr"
LIEN_ALEATOIRE = "http://m.viedemerde.fr/aleatoire"
LIEN_PAGE = "http://m.viedemerde.fr/?page=%s"
LIEN_ARTICLE = "http://m.viedemerde.fr/%s"

class VdmCrawler(ArticleCrawler):
	"""The implementation of VieDeMerde crawler"""
	def __init__(self):
		super().__init__(VdmParser(), HttpCommunicator())
	def __go(self, lien):
		reponse = self.aspirateur.get(lien)
		if reponse["code"] == 200:
			text = unescape(reponse["data"]).replace("&quot;", "'")
			data = self.parser.parse(text)
			code = 200
		else:
			code = reponse["code"]
			data = []
		return (code, data)
	def page(self, id_):
		global LIEN_PAGE
		(code, data) = self.__go(LIEN_PAGE % (id_))
		return ResponseCrawler(code,data)
	def article(self, id_):
		global LIEN_ARTICLE
		(code, data) = self.__go(LIEN_ARTICLE % id_)
		return ResponseCrawler(code,data)
	def page_random(self):
		global LIEN_ALEATOIRE
		(code, data) = self.__go(LIEN_ALEATOIRE)
		return ResponseCrawler(code,data)
	def article_random(self):
		global LIEN_ALEATOIRE
		(code, data) = self.__go(LIEN_ALEATOIRE)
		if len(data) > 0:
			data = [data[0]]
		return ResponseCrawler(code, data)
