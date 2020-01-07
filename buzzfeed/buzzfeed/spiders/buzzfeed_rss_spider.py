import scrapy
import feedparser

import os
import re
import json

from colorama import Fore, init
init()

class RssSpider(scrapy.Spider):
    name = 'rss'

    def start_requests(self):
        input = getattr(self, 'input', None)
        if input is None:
            raise RuntimeError(Fore.RED + 'Input file has not been provided.' + Fore.RESET)

        with open(os.path.join(os.getcwd(), input), 'r') as f:
            for url in f.read().split('\n'):
                if url != '':
                    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        category = re.findall(r'/(\w+).xml', response.url)[0]
        for page_num in range(1, 6):
            entries = feedparser.parse(response.url + '?page=' + str(page_num)).entries
            for entry in entries[:250]:
                try:
                    summary = re.findall('<h1>(.*)<\/h1>', entry.summary)[0]
                except IndexError:
                    summary = 'NaN'

                try:
                    yield {
                        'title': entry.title,
                        'summary': summary,
                        'author': entry.author,
                        'link': entry.link,
                        'published': entry.published,
                        'category': category
                    }

                    with open(os.path.join(os.getcwd(), 'links_articles.txt'), 'a') as f:
                        f.write(entry.link + '\n')
                except AttributeError:
                    pass
