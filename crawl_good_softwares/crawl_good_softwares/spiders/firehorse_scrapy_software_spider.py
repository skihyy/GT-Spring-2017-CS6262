# -*- coding: utf-8 -*-
import scrapy
import urllib
import os
from scrapy.http import Request
from scrapy.selector import Selector
from crawl_good_softwares.items import CrawlGoodSoftwaresItem


class TestSpiderSpider(scrapy.Spider):
    name = "firehorse_scrapy_software_spider"
    start_urls = ['http://www.filehorse.com/popular/',
                  'http://www.filehorse.com/latest/',
                  'http://www.filehorse.com/software-benchmarking/',
                  'http://www.filehorse.com/software-compression-and-backup/']
    current_page = 1
    max_page = 6

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    def __init__(self, *a, **kw):
        while self.current_page < self.max_page:
            self.current_page = self.current_page + 1
            link = 'http://www.filehorse.com/popular/page-' + str(self.current_page)
            link2 = 'http://www.filehorse.com/latest/page-' + str(self.current_page)
            link3 = 'http://www.filehorse.com/software-benchmarking/page-' + str(self.current_page)
            link4 = 'http://www.filehorse.com/software-compression-and-backup/page-' + str(self.current_page)
            self.start_urls.append(link)
            self.start_urls.append(link2)
            self.start_urls.append(link3)
            self.start_urls.append(link4)
        super(scrapy.Spider, self).__init__(*a, **kw)

    def parse(self, response):
        selector = Selector(response)
        software_links = selector.xpath('//div[@class="cat_dl_btn"]/a/@href').extract()
        if 0 < len(software_links):
            for link in software_links:
                yield Request(link, callback=self.parse, headers=self.headers)
        else:
            final_download_url = selector.xpath('//a[@id="download_url"]/@href').extract()
            if 0 == len(final_download_url):
                yield Request(response.url + 'download/', callback=self.parse, headers=self.headers)
            else:
                item = CrawlGoodSoftwaresItem()
                item['link'] = final_download_url[0]
                yield item
