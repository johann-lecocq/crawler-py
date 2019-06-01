#!/usr/bin/python
import argparse
from sys import exit

from crawlerpy.dtc import DtcCrawler
from crawlerpy.scmb import ScmbCrawler
from crawlerpy.vdm import VdmCrawler


def affiche_article(article):
    print(article.id, ":")
    for section in article.sections:
        for data in section.contents:
            print(section.id," ", data.value)
    print()


crawlers = {
    "vdm": VdmCrawler(),
    "dtc": DtcCrawler(),
    "scmb": ScmbCrawler()
}

parser = argparse.ArgumentParser()
parser.add_argument('crawler', action="store", help="dtc(danstonChat.com),vdm(viedemerde.fr)")
parser.add_argument('action', action="store", help="page, article, random")
parser.add_argument('--number', action="store", default=0, help="numero de la page ou de l'article")

args = parser.parse_args()

if args.crawler not in crawlers:
    print("The crawler is not valid")
    exit(1)

crawler = crawlers[args.crawler]
actions = {
    "page": crawler.page,
    "article": crawler.article,
    "random": crawler.random}

if args.action not in actions:
    print("The action is not valid")
    exit(2)

if args.action == "page" or args.action == "article":
    code,reponse = actions[args.action](args.number)
else:
    code,reponse = actions[args.action]()

if code != 200:
    print("Error", reponse)
    exit(3)

if args.action == "article":
    affiche_article(reponse)
else:
    for article in reponse:
        affiche_article(article)
