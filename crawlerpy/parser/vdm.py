# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"
__version__ = "1.3"

from re import findall,I,U

from crawlerpy.parser import Parser,ParseException
from crawlerpy.objet import *

class VdmParser(Parser):
	"""The implementation of VideDeMerde site parser"""
	def __init__(self):
		pass
	def parse(self,text):
		try:
			reponse=[]
			text=text.replace("&quot;","'")
			l=findall(u"<li id=\"fml-(\d+)\">.*(Aujourd'hui,[-\d\w\s,.;:!'\"’+&?—()]*VDM)",text,I|U)
			for i in l:
				section=Section("text")
				section.add_content(Data("string",i[1]))
				article=Article(i[0])
				article.add_section(section)
				reponse.append(article)
			return reponse
		except Exception:
			raise ParseException()
