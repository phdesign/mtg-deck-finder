# pylint: disable=line-too-long
import os
import sys
from urllib.parse import urlparse, parse_qs
import scrapy


class TappedOutSpider(scrapy.Spider):
    name = "tappedout"

    custom_settings = {
        # 'EXTENSIONS': {
        # 'scrapy.extensions.closespider.CloseSpider': 500
        # },
        # 'CLOSESPIDER_PAGECOUNT': 10,
        # 'CONCURRENT_REQUESTS': 1,
        "DOWNLOAD_DELAY": 0.15,
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
        yield scrapy.Request(
            url="http://tappedout.net/mtg-decks/search/", callback=self.parse
        )

    def parse(self, response):
        for deck in response.css("h3.name a"):
            yield response.follow(deck, callback=self.parse_deck)
        next_page = response.css(".pagination")[0].css("li.active + li a")[0]
        yield response.follow(next_page, callback=self.parse)

    def parse_deck(self, response):
        download = response.url + "?fmt=txt"
        filepath = self._get_filepath(response.url)
        if filepath and not os.path.exists(filepath):
            yield response.follow(download, callback=self.parse_download)

    def parse_download(self, response):
        filepath = self._get_filepath(response.url)
        print(f"saving {filepath}...", file=sys.stderr)
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.body)

    def _get_filepath(self, url):
        path = urlparse(url).path
        pathparts = path.strip("/").rsplit("/", maxsplit=1)
        name = pathparts[1]
        if not name:
            return None
        filename = self._safename(name) + ".txt"
        base_folder = getattr(self, "folder", ".")
        return os.path.join(base_folder, self.name, filename)

    def _safename(self, filename):
        keepcharacters = (" ", ".", "_", "-")
        return "".join(
            c for c in filename if c.isalnum() or c in keepcharacters
        ).rstrip()
