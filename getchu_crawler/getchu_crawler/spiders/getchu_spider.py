import scrapy
import sys
from getchu_crawler.items import GetchuCrawlerItem
from scrapy.http import Request
from scrapy.selector import Selector
import json
# reload(sys)
# sys.setdefaultencoding('utf-8')


class GetchuCrawlerSpider(scrapy.Spider):
    name = "getchu_crawler"  # spider 이름
    allowed_domains = ["www.getchu.com"]  # 크롤링할 최상위 도메인
    # ori_start_urls = ["http://www.getchu.com/php/search.phtml?search_keyword=&search_title=&search_brand=&search_person=&search_jan=&search_isbn=&genre=pc_soft&start_date=2014/01/01&end_date=2018/12/31&age=all&list_count=100&sort=release_date&sort2=up&list_type=list&search=1&pageID="
    #                   + str(i+1) for i in range(30)]
    # # start_urls = ["http://www.getchu.com/soft.phtml?id=986010&gc=gc"]
    # start_urls = []
    # for urls in ori_start_urls:
    #     start_urls.append(urls + "&gc=gc")
    # print('start')
    file = open('Getchu_2014_2018.json', 'r', encoding='utf-8')
    start_urls = json.loads(file.read())

    def __init__(self):
        super().__init__()
        self.game_urls = []

    def save_urls(self):
        file = open('Getchu_2014_2018.json', 'w', encoding='utf-8')
        line = json.dumps(self.game_urls) + "\n"
        file.write(line)

    def parse(self, response):
        # print('parse')
        # urls = response.xpath(
        #     '//*[@class="blueb"]/@href'
        # ).extract()
        #
        # for url in urls:
        #     self.game_urls.append("http://www.getchu.com/" + url.split('/')[1] + "&gc=gc")
        # print(len(self.game_urls))
        # self.save_urls()

        image_urls = response.xpath(
            '//a[contains(@name, "chara")]/following-sibling::img/@src'
        ).extract()
        chara_names = response.xpath(
            '//a[contains(@name, "chara")]/parent::td/following-sibling::td//*[@class="chara-name"]/text()'
        ).extract()
        year = response.xpath(
            '//a[@id="tooltip-day"]/text()'
        ).extract()
        if image_urls:
            image_urls = [response.urljoin(url) for url in image_urls]
            chara_names = list(zip(chara_names, image_urls))
            yield GetchuCrawlerItem(
                game_url=response.url,
                chara_names=chara_names,
                image_urls=image_urls,
                year=year)
        else:
            yield GetchuCrawlerItem(game_url=response.url)