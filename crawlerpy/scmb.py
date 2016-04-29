# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from html import unescape

from crawlerpy import ArticleCrawler, HttpCommunicator, ResponseCrawler
from crawlerpy.parser import ParseException
from crawlerpy.parser.scmb import ScmbParser

LIEN_ACCUEIL="http://secouchermoinsbete.fr"
LIEN_ALEATOIRE="http://secouchermoinsbete.fr/random"
LIEN_PAGE="http://secouchermoinsbete.fr/?page=%s"
LIEN_ARTICLE="http://secouchermoinsbete.fr/%s"

class ScmbCrawler(ArticleCrawler):
	"""The implementation of VieDeMerde crawler"""
	def __init__(self):
		super().__init__(ScmbParser(),HttpCommunicator())
	def __go(self,lien):
		print(lien)
		reponse=self.aspirateur.get(lien)
		if reponse["code"]==200:
			text=unescape(reponse["data"])
			try:
 				data=self.parser.parse(text)
			except ParseException:
				return(521,[])
			code=200
		else:
			code=reponse["code"]
			data=[]
		return (code, data)
	def page(self,id_):
		global LIEN_PAGE
		(code, data) = self.__go(LIEN_PAGE % (id_+1))
		return ResponseCrawler(code,data)
	def article(self,id_):
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
