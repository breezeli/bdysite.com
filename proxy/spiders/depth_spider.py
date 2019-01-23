import scrapy
from urllib import parse
from proxy.items import ArticleItem

# 定制化爬虫
class DeptSpdier(scrapy.Spider):
    # 爬虫名称
    name = "depth"
    start_urls = ["http://www.fkzww.net/forum-4-1.html"]
    allowed_domains = ["www.fkzww.net"]

    # 列表解析
    def parse(self, response):
        self.logger.debug("depth parser url:%s", response.url)
        # 分页
        page_urls = response.xpath("//div[@class='pages']/a/@href").extract()
        # 遍历所有分页
        for url in page_urls:
            yield scrapy.Request(url=parse.urljoin(response.url, url), callback=self.parse)

        # detail详情
        detail_urls = response.xpath("//th//a[contains(@href,'thread')]/@href").extract()
        # 遍历所有详情地址
        for url in detail_urls:
            yield scrapy.Request(url=parse.urljoin(response.url, url), callback=self.parser_detail)

    # 内容解析
    def parser_detail(self, response):
        self.logger.debug("depth parser detail url:%s", response.url)
        # 查找内容标签
        td = response.xpath("//td[@class='t_msgfont']")
        # 定义item
        item = ArticleItem()
        # 标题
        item["title"] = response.xpath("//title/text()").extract()
        # 链接地址
        item["url"] = response.url
        # 解析图片地址（部分内容中仅有图片），所以单独解析和抓取内容中的图片
        img = td.xpath("//img[contains(@file,'attachments/month')]/@file").extract()
        if len(img) > 0:
            # 图片地址格式化
            item["img"] = parse.urljoin(response.url, img[0])
        else:
            # 避免插入数据便利为空
            item["img"] = ""

        # 获取文章中的所有文本信息
        text = td.xpath("string(.)").extract()
        if len(text):
            item["content"] = text[0]
        else:
            # 避免插入数据便利为空
            item["content"] = ""

        yield item
