# -*- coding: utf-8 -*-
import scrapy
import urllib
import os
from selenium import webdriver
from scrapy.http import Request


class TestSpiderSpider(scrapy.Spider):
    name = "phantom_software_spider"
    start_urls = ['http://download.cnet.com/s/software/windows-free/?sort=most-popular']
    current_page = 1
    max_page = 1

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # using selenium + PhantomJS to simulate Chrome since directly use Chrome is tooooo slow
    # also, using Chrome need Chrome driver
    # using firefox need firefox
    driver = webdriver.PhantomJS()

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, headers=self.headers)
        '''
        for i in range(1, 2):
            url = self.start_urls[0]
            if 1 != i:
                url = url + str(i)
        '''

    def parse(self, response):
        # using PhantomJS to reloaded the web page
        # get JS rendered page
        self.driver.get(response.url)
        software_links = self.driver.find_elements_by_xpath('//a[@data-position]')
        if software_links:
            # it is a download list page
            for link in software_links:
                href = link.get_attribute('href')
                yield Request(href, callback=self.parse, headers=self.headers)
        else:
            # it is a download page
            tmp_name = self.driver.title.split(' ')
            file_name = ''
            for name in tmp_name:
                if '-' != name:
                    file_name = file_name + name
            file_name = file_name + 'a.exe'
            file_path = os.path.join('./app_download/', file_name)
            download_url = self.driver.find_element_by_xpath('//a[@class="dln-a"]')
            download_href = download_url.get_attribute('data-href')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            print(download_href)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            urllib.urlretrieve(download_href, file_path)

    def __del__(self):
        self.driver.quit()
