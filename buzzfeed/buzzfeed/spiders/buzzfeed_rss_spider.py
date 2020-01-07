import scrapy
import feedparser
from bs4 import BeautifulSoup

import os
import re
import json
import sys

import urllib.request

from colorama import Fore, init
init()

class RssSpider(scrapy.Spider):
    name = 'rss'

    def start_requests(self):
        self.article_id = 0
        input = getattr(self, 'input', None)
        if input is None:
            raise RuntimeError(Fore.RED + 'Input file has not been provided.' + Fore.RESET)

        with open(os.path.join(os.getcwd(), input), 'r') as f:
            for url in f.read().split('\n'):
                if url != '':
                    yield scrapy.Request(url=url, callback=self.parse)

    def load_text(self, url):
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html)
        texts = []

        # Parsing text areas
        for div in soup.findAll('div', attrs={'class': 'subbuzz-text'}):
            for p in div.findAll('p'):
                texts.append(p.get_text())

        # Parsing description areas
        for div in soup.findAll('div', attrs={'class': 'subbuzz__description'}):
            for p in div.findAll('p'):
                texts.append(p.get_text())

        # Parsing sub titles
        for span in soup.findAll('span', attrs={'class': 'js-subbuzz__title-text'}):
            texts.append(span.get_text())

        # limit = int(getattr(self, 'limit', 2000))
        return ' '.join(texts)[:2000]

    def parse(self, response):
        category = re.findall(r'/(\w+).xml', response.url)[0]
        for page_num in range(1, 6):
            entries = feedparser.parse(response.url + '?page=' + str(page_num)).entries
            for entry in entries[:200]:
                try:
                    summary = re.findall('<h1>(.*)<\/h1>', entry.summary)[0]
                except IndexError:
                    summary = 'NaN'

                try:
                    text = self.load_text(response.url)
                except:
                    text = None

                print('Parsing article #{}'.format(self.article_id))

                try:
                    yield {
                        'id': self.article_id,
                        'title': entry.title,
                        'summary': summary,
                        'text': text,
                        'author': entry.author,
                        'link': entry.link,
                        'published': entry.published,
                        'category': category
                    }

                except AttributeError:
                    pass

                self.article_id += 1
