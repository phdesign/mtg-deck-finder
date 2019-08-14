# pylint: disable=line-too-long
import os
import sys
import re
import json
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import scrapy


class WizardsSpider(scrapy.Spider):
    name = "wizards"

    custom_settings = {
        # "EXTENSIONS": {"scrapy.extensions.closespider.CloseSpider": 500},
        # "CLOSESPIDER_PAGECOUNT": 10,
        # "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 0.50,
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
            url="https://magic.wizards.com/en/section-articles-see-more-ajax?l=en&f=9041&search-result-theme=&limit=20&fromDate=&toDate=&sort=DESC&word=&offset=0",
            callback=self.parse,
        )

    def parse(self, response):
        body = json.loads(response.body_as_unicode())
        for item in body["data"]:
            decoded = bytes(item, "utf-8").decode("unicode_escape")
            match = re.search('href="(.*?)"', decoded)
            yield response.follow(match.group(1), callback=self.parse_decklist)

        if body["displaySeeMore"] == 1:
            new_url = self._get_next_url(response.url, body["offset"])
            yield scrapy.Request(url=new_url, callback=self.parse)

    def parse_decklist(self, response):
        for deck in response.css(".bean_block_deck_list"):
            self._parse_deck(deck)

    def _get_next_url(self, url, offset):
        scheme, netloc, path, params, query, fragment = urlparse(url)
        qs = parse_qs(query)
        qs["offset"] = offset
        query = urlencode(qs, doseq=True)
        return urlunparse((scheme, netloc, path, params, query, fragment))

    def _parse_deck(self, deck):
        title = deck.css(".deck-meta h4::text").get()
        main = deck.css(".sorted-by-overview-container .row")
        sideboard = deck.css(".sorted-by-sideboard-container .row")

        main_cards = [(x.css(".card-count::text").get(), x.css(".card-name a::text").get()) for x in main]
        sideboard_cards = [(x.css(".card-count::text").get(), x.css(".card-name a::text").get()) for x in sideboard]

        output = "\n".join(f"{count} {name}" for (count, name) in main_cards)
        output += "\n\n"
        output += "\n".join(f"{count} {name}" for (count, name) in sideboard_cards)

        filepath = self._get_filepath(title)
        if not os.path.exists(filepath):
            print(f"saving {filepath}...", file=sys.stderr)
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w") as f:
                f.write(output)
        else:
            print(f"skipping {filepath}...", file=sys.stderr)

    def _get_filepath(self, title):
        filename = self._safename(title) + ".txt"
        base_folder = getattr(self, "folder", ".")
        return os.path.join(base_folder, self.name, filename)

    def _safename(self, filename):
        return filename.translate(str.maketrans("", "", r'\/:*?"<>|')).strip()
