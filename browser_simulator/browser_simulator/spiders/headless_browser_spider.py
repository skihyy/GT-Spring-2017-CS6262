# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.http import Request
from browser_simulator.items import BrowserSimulatorItem
import pdb

class TestSpiderSpider(scrapy.Spider):
    name = "headless_spider"
    # allowed_domains = ["yuyang.bid/"]
    start_urls = ['https://yuyang.bid/CS6262_test/html_redirects/r1.html']

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': True,  # no redirect
        'handle_httpstatus_list': [301, 302]  # handle exceptions
    }

    # using selenium + PhantomJS to simulate Chrome since directly use Chrome is tooooo slow
    # also, using Chrome need Chrome driver
    # using firefox need firefox
    driver = webdriver.PhantomJS()

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, headers=self.headers, meta=self.meta)

    def parse(self, response):
        # using PhantomJS to reloaded the web page
        # get JS rendered page
        self.driver.get(response.url)
        # will not use 'selector = Selector(response)'
        item = BrowserSimulatorItem()
        # used for search redirect
        item['raw_data'] = self.driver.page_source
        item['url'] = response.url
        # now just get some header
        item['header'] = response.headers.getlist('Set-Cookie')
        item['body'] = self.driver.find_element_by_xpath('//body/*')
        # only do the html redirect now
        redirect_element = self.driver.find_element_by_xpath('//meta[@http-equiv="refresh" and @content]')
        tmp_redirect = redirect_element.get_attribute("content")
        redirect_result = ''
        if tmp_redirect:
            redirect_result = self.redirect_handler(tmp_redirect, response.url)
            yield Request(redirect_result, callback=self.parse, headers=self.headers, meta=self.meta)
        item['redirect'] = redirect_result
        all_links = self.driver.find_elements_by_xpath('//a/@content')
        item['links'] = self.links_handler(all_links)
        yield item

    def redirect_handler(self, redirect, cur_url):
        # e.g. '0.5;url=http://helloworld.com'
        # e.g. '0.5;url=empty.exe'
        # after split, only need 'empty.exe'
        redirect_part = redirect.split('url=')[1]
        redirect_head = ''
        # it is already a link
        if redirect_part.startswith('http'):
            final_url = redirect_part
        # if just a part of link
        else:
            url_pieces = cur_url.split('/')
            for i in range(0, len(url_pieces) - 1):
                if 0 == i:
                    if url_pieces[i].startswith('http'):
                        redirect_head += url_pieces[i]
                        redirect_head += '/'
                        redirect_head += '/'
                    else:
                        redirect_head += 'http://'
                        redirect_head += url_pieces[i]
                        redirect_head += '/'
                elif 0 < len(url_pieces[i]):
                    redirect_head += url_pieces[i]
                    redirect_head += '/'
            final_url = redirect_head + redirect_part
        return final_url.encode('ascii', 'ignore')

    def links_handler(self, links):
        result = ''
        for link in links:
            result += link + ','
        return result

    def __del__(self):
        self.driver.quit()
