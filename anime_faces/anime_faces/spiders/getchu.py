# -*- coding: utf-8 -*-
import json
import os

import scrapy

from anime_faces.items import AnimeFacesItem


class GetchuSpider(scrapy.Spider):
    name = 'getchu'
    allowed_domains = ['getchu.com']

    def load_urls(self, input_path):
        with open(input_path) as infile:
            sources = {line.strip().split()[-1] for line in infile}
        sources = sorted(sources)
        return sources

    def load_visited(self, output_path):
        if os.path.exists(output_path):
            with open(output_path) as infile:
                visited = {json.loads(line)['game_url'] for line in infile}
        else:
            visited = set()
        return visited

    def __init__(self, input_path, output_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sources = self.load_urls(input_path)
        self.visited = self.load_visited(output_path)

    def start_requests(self):
        for url in self.sources:
            if url not in self.visited:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        image_urls = response.xpath(
            '//a[contains(@name, "chara")]/following-sibling::img/@src'
        ).extract()
        chara_names = response.xpath(
            '//a[contains(@name, "chara")]/parent::td/following-sibling::td//*[@class="chara-name"]/text()'
        ).extract()

        if image_urls:
            image_urls = [response.urljoin(url) for url in image_urls]
            chara_names = list(zip(chara_names, image_urls))

            yield AnimeFacesItem(
                game_url=response.url,
                chara_names=chara_names,
                image_urls=image_urls)
        else:
            yield AnimeFacesItem(game_url=response.url)
