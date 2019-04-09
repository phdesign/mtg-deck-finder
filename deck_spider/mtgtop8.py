import os
import re
from urllib.parse import urlparse, parse_qs
import scrapy

class MtgTop8Spider(scrapy.Spider):
    name = 'mtgtop8'

    # custom_settings = {
        # 'EXTENSIONS': {
            # 'scrapy.extensions.closespider.CloseSpider': 500
        # },
        # 'CLOSESPIDER_PAGECOUNT': 20,
        # 'CONCURRENT_REQUESTS': 1
    # }

    def start_requests(self):
        yield scrapy.Request(url='http://www.mtgtop8.com/search', callback=self.parse_search)

    def parse_search(self, response):
        for deck in response.css('.S11 a'):
            yield response.follow(deck, callback=self.parse_card)
        next_page_num = response \
            .css('[name=compare_decks] table table tr:first-of-type td:last-of-type .Nav_PN::attr(onclick)') \
            .re(r"PageSubmit\((\d+)\)")
        if next_page_num:
            data = {'current_page': next_page_num[0]}
            yield scrapy.FormRequest(response.url, formdata=data, callback=self.parse_search)

    def parse_card(self, response):
        download = response.css('.Nav_link a')[0]
        yield response.follow(download, callback=self.parse_download)

    def parse_download(self, response):
        filename = parse_qs(urlparse(response.url).query).get("f")[0] + '.txt'
        base_folder = getattr(self, 'folder', '.')
        filepath = os.path.join(base_folder, self.name, filename)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(response.body)
