# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from re import findall,I,U
from crawlerpy.parser import Parser,ParseException
from crawlerpy.objet import *

class DtcParser(Parser):
	"""The implementation of DansTonChat site parser"""
	def __init__(self):
		pass
	def parse(self,text):
		try:
			reponse=[]
			for i in findall(u"<div class=\"item item(\d+)\">(.*?)<p class=\"item-meta\">",text,I|U):
				id_=i[0]
				text=i[1]
				text=text.replace("<p class=\"item-content\"><a href=\"https://danstonchat.com/"+id_+".html\">","")
				text=text.replace("</a></p>","")
				text=text.replace("<span class=\"decoration\">","")
				text=text.replace("</span>","")
				liste=text.split("<br />")
				article=Article(id_)
				section=Section("quote")
				for i in liste:
					section.add_content(Data("string",i))
				article.add_section(section)
				reponse.append(article)
			return reponse
		except Exception as e:
			print(e)
			raise ParseException()
