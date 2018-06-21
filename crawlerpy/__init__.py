# -*- coding: utf-8 -*-

__author__="Johann Lecocq(johann-lecocq.fr)"
__license__ = "GNU GENERAL PUBLIC LICENSE version 2"

from urllib.request import urlopen,HTTPError,URLError,Request
from urllib.error import URLError

class Communicator:
    """interface of a Communicator"""
    def get(self,lien):
        """return a dict
        response code(required)->integer
        data(required)"""
        pass

class HttpCommunicator(Communicator):
    """Implementation of Communicator for HTTP"""
    def __init__(self):
        pass
    def get(self,lien):
        code=200
        text=""
        try:
            req = Request(
                lien,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
                }
            )
            f = urlopen(req)
            information=f.read()
            f.close()
            code=f.getcode()
            text=information.decode("utf-8")
        except HTTPError as e:
            code=e.code
            text=""
        except URLError:
            code=404
            text=""
        return {"code":code,"data":text}


class ArticleCrawler:
    """Represent an ArticleCrawler"""
    def __init__(self,parser,aspirateur):
        self.parser=parser
        self.aspirateur=aspirateur
    def page(self,id_):
        """return ResponseCrawler all article of the page
            id_ identfiant of the page
        """
        pass
    def article(self,id_):
        """return ResponseCrawler article identified by id_
            id_ identfiant of the article
        """
        pass
    def page_random(self):
        """return ResponseCrawler all article of a random page
            id_ identfiant of the article
        """
        pass
    def article_random(self):
        """return ResponseCrawler  a random article
            id_ identfiant of the article
        """
        pass


class ResponseCrawler:
    """ It's an object return by a crawler
        code-> 0 if OK else 1 to NOT OK"""
    def __init__(self,code,data):
        self.code=code
        self.data=data
