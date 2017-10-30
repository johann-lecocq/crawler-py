# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from re import findall,I,U,DOTALL
from crawlerpy.parser import Parser,ParseException
from crawlerpy.objet import *

class DtcParser(Parser):
	"""The implementation of DansTonChat site parser"""
	def __init__(self):
		pass
	def parse(self,text):
		try:
			reponse=[]
			for ident,quote in findall('<a href="https://danstonchat\.com/(\d+)\.html">(.*?)</a>',text,I|U|DOTALL):
				quote = quote.strip() +"<br />"
				article=Article(ident)
				section=Section("quote")
				elements = findall('<span class="decoration" style="background-color: RGB\(\d{3},\d{3},\d{3}\);">(.*?)</span>(.*?)<br />',quote,I|U|DOTALL)
				#print(ident,"->",elements)
				for pseudo, text in elements:
					section.add_content(Data("string",pseudo.strip()+" "+text.strip()))
				if elements:
					article.add_section(section)
					reponse.append(article)
			return reponse
		except Exception as e:
			print(e)
			raise ParseException()
