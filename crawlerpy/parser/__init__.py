# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

class ParseException(Exception):
	pass

class Parser:
	"""interface of Parser"""
	def parse(self,text):
		"""return a list of Article"""
		pass
