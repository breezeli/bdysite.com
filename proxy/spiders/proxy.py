import scrapy
import json
from proxy.items import ProxyItem


class ProxyValidateSpider(scrapy.Spider):
    name = "proxy"
    start_urls = {"http://www.fkzww.net/forum-4-1.html"}

    def parse(self,response):
        print(response.body)

        data = json.loads(response.body)

        item = ProxyItem()

        item["name"] = data["DOCUMENT_ROOT"]
        item["ip"] = data["REMOTE_ADDR"]
        yield item