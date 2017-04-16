# -*- coding: utf-8 -*-
import scrapy
import urllib
import os
from scrapy.http import Request
from scrapy.selector import Selector
from selenium import webdriver



class TestSpiderSpider(scrapy.Spider):
    name = "final_software_spider"
    start_urls = ['http://download.cnet.com/s/software/windows-free/?sort=most-popular&page=']
    current_page = 1
    max_page = 1

    # driver = webdriver.Chrome()

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    def parse(self, response):
        selector = Selector(response)
        software_links = selector.xpath('//a[@data-position]/@href').extract()
        if 0 < len(software_links):
            for link in software_links:
                yield Request(link, callback=self.parse, headers=self.headers)
        else:
            tmp_name = selector.xpath('//title/text()').extract().split(' ')
            file_name = ''
            for name in tmp_name:
                if '-' != name:
                    file_name = file_name + name
            file_name = file_name + 'a.exe'
            file_path = os.path.join('./app_download/', file_name)
            download_url = selector.xpath('//a[@class="dln-a"]/@data-href').extract()
            download_href = download_url[0]
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print(download_href)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            urllib.urlretrieve(download_href, file_path)
