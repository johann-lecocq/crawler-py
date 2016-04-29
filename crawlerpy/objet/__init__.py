# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

class Article:
	"""
		Representation of an article
		an identifiant
		the publish date of the article
		the categorie of the article
		list of section
	"""
	def __init__(self,identifiant,publish_date=None,categorie=None):
		self.identifiant=identifiant
		self.publish_date=publish_date
		self.categorie=categorie
		self.sections=[]
	def add_section(self,section):
		"""add a section in the article"""
		self.sections.append(section)

class Section:
	"""represent a part of an article
		identifiant:the name of part
		contains list of data
	"""
	def __init__(self,identifiant):
		self.identifiant=identifiant
		self.content=[]
	def add_content(self,data):
		"""add a content to the Section"""
		self.content.append(data)

class Data:
	"""Represent a data
		type-> the type of data
		value-> the value"""
	def __init__(self,type_,value):
		self.type=type_
		self.value=value
