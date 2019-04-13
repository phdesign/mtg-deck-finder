import os
import sys
from urllib.parse import urlparse, parse_qs
import scrapy

class MtgTop8Spider(scrapy.Spider):
    name = 'mtgtop8'

    custom_settings = {
        # 'EXTENSIONS': {
            # 'scrapy.extensions.closespider.CloseSpider': 500
        # },
        # 'CLOSESPIDER_PAGECOUNT': 10,
        # 'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 0.25,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',  # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',  # chrome
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',  # firefox
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36',  # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36',  # chrome
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',  # chrome
        ]
    }

    def start_requests(self):
        yield scrapy.Request(url='http://www.mtgtop8.com/search', callback=self.parse)

    def parse(self, response):
        for deck in response.css('.S11 a'):
            yield response.follow(deck, callback=self.parse_card)
        next_page_num = response \
            .css('[name=compare_decks] table table tr:first-of-type td:last-of-type .Nav_PN::attr(onclick)') \
            .re(r"PageSubmit\((\d+)\)")
        if next_page_num:
            data = {'current_page': next_page_num[0]}
            yield scrapy.FormRequest(response.url, formdata=data, callback=self.parse)

    def parse_card(self, response):
        download = response.css('.Nav_link a')[0]
        filepath = self._get_filepath(download.attrib['href'])
        if filepath and not os.path.exists(filepath):
            yield response.follow(download, callback=self.parse_download)

    def parse_download(self, response):
        filepath = self._get_filepath(response.url)
        print(f"saving {filepath}...", file=sys.stderr)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(response.body)

    def _get_filepath(self, url):
        querystring = urlparse(url).query
        if not querystring:
            return None
        name = parse_qs(querystring).get("f")
        if not name:
            return None
        filename = self._safename(name[0]) + '.txt'
        base_folder = getattr(self, 'folder', '.')
        return os.path.join(base_folder, self.name, filename)

    def _safename(self, filename):
        keepcharacters = (' ', '.', '_')
        return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()
