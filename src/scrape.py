import os
from string import ascii_uppercase

from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy.selector import Selector
from w3lib.html import remove_tags

DEF_MAX_SCRIPTS = 20


class ScriSpider(Spider):
    name: str = "scripts"
    maxNum = 0
    start_urls = [
        "https://www.imsdb.com/alphabetical/" + a for a in list("0" + ascii_uppercase)
    ]

    def parse(self, response: Response):
        self.num = 0
        for nextPage in response.xpath(
            "//a[@title and starts-with(@href, '/Movie Scripts/')]/@href"
        ).extract():
            if self.num < self.maxNum:
                yield Request(response.urljoin(nextPage), callback=self.getScript)

    def getScript(self, response: Response):
        if self.num < self.maxNum:
            scriptLink = response.xpath(
                "//a[starts-with(@href, '/scripts/')]/@href"
            ).extract_first()
            if scriptLink.endswith("html"):
                yield Request(response.urljoin(scriptLink), callback=self.readScript)

    def readScript(self, response: Response):
        if self.num < self.maxNum:
            script = response.xpath("//td[@class='scrtext']/pre").extract_first()
            if not script:
                script = response.xpath("//td[@class='scrtext']").extract_first()
            if script:
                if not os.path.exists("data"):
                    os.mkdir("data")
                with open("data/script" + str(self.num) + ".txt", "w+") as f:
                    f.write(remove_tags(script))
                    self.num += 1


def scrape(numScripts: int):
    ScriSpider.maxNum = numScripts
    process = CrawlerProcess(
        {"USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"}
    )
    process.crawl(ScriSpider)
    process.start()


if __name__ == "__main__":
    scrape(DEF_MAX_SCRIPTS)
