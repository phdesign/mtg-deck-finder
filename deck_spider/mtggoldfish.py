# pylint: disable=line-too-long
import os
import sys
import re
from urllib.parse import urlparse
import scrapy


class MtgGoldfishSpider(scrapy.Spider):
    name = "mtggoldfish"

    custom_settings = {
        # "EXTENSIONS": {"scrapy.extensions.closespider.CloseSpider": 500},
        # "CLOSESPIDER_PAGECOUNT": 10,
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 1.00,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware": 500,
        },
        "USER_AGENTS": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36",  # chrome
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36",  # chrome
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",  # firefox
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",  # chrome
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",  # chrome
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",  # chrome
        ],
    }

    def start_requests(self):
        yield scrapy.Request(url="https://www.mtggoldfish.com/deck/custom/standard#paper", callback=self.parse)

    def parse(self, response):
        for deck in response.css(".deck-tile .deck-price-paper a"):
            yield response.follow(deck, callback=self.parse_deck)

        next_page = response.css(".pagination a.next_page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for deck in response.css(".deck-price-paper .subNav-menu-desktop a"):
            yield response.follow(deck, callback=self.parse)

    def parse_deck(self, response):
        try:
            download = response.css(".deck-view-tools .btn")[4]
            yield response.follow(download, callback=self.parse_download)
        except IndexError:
            print(f"no download link", file=sys.stderr)

    def parse_download(self, response):
        filepath = self._get_filepath(response)
        if not os.path.exists(filepath):
            print(f"saving {filepath}...", file=sys.stderr)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(response.body)
        else:
            print(f"skipping {filepath}...", file=sys.stderr)

    def _get_filepath(self, response):
        content_disposition = response.headers.get("Content-Disposition").decode("utf-8")
        filename = content_disposition.split(";")[1].split("=")[1]
        filename = filename.strip("\"'")
        if not filename:
            return None
        filename = self._safename(filename)
        base_folder = getattr(self, "folder", ".")
        return os.path.join(base_folder, self.name, filename)

    def _safename(self, filename):
        return filename.translate(str.maketrans("", "", r'\/:*?"<>|')).strip()
