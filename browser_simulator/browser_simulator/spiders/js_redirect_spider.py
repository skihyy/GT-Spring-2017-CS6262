# -*- coding: utf-8 -*-
# This spider is used for HTML redirect crawling
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import Request
from browser_simulator.items import BrowserSimulatorItem


class TestSpiderSpider(scrapy.Spider):
    name = "js_redirect_spider"
    # allowed_domains = ["yuyang.bid/"]
    start_urls = ['https://yuyang.bid/CS6262_test/js_redirects/r1.html']

    headers = {
        'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    meta = {
        'dont_redirect': True,  # no redirect
        'handle_httpstatus_list': [301, 302]  # handle exceptions
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse, headers=self.headers, meta=self.meta)

    def parse(self, response):
        item = BrowserSimulatorItem()
        # used for search redirect
        selector = Selector(response)
        raw_data = selector.xpath('//html/*').extract()
        item['raw_data'] = raw_data
        item['url'] = response.url
        # now just get some header
        item['header'] = response.headers.getlist('Set-Cookie')
        item['body'] = selector.xpath('//body/*').extract()
        # only do the js redirect now
        # 1 - JS is embed in HTML
        tmp_redirect = ''
        redirect_result = ''
        for js in raw_data:
            # there is a redirect
            if "window.location.href" in js:
                redirect_js = re.findall("window.location.href*=*'.*.'", js)[0].encode('ascii', 'ignore')
                tmp_redirect = re.findall("'.*.'", redirect_js)[0].encode('ascii', 'ignore')
                # now there is quotation mark in tmp_redirect
                tmp_redirect = tmp_redirect[1: len(tmp_redirect) - 1]
                break

        # 2 - JS is linked to another file
        # go to that file to find
        if not tmp_redirect:
            js_file_location = selector.xpath('//script[@type="text/javascript" and @src]/@src').extract()
            for file_src in js_file_location:
                redirect_result = self.redirect_handler(file_src, response.url)
                yield Request(redirect_result, callback=self.parse, headers=self.headers, meta=self.meta)
        else:
            redirect_result = self.redirect_handler(tmp_redirect, response.url)
            yield Request(redirect_result, callback=self.parse, headers=self.headers, meta=self.meta)
        item['redirect'] = redirect_result
        all_links = selector.xpath('//a/@content').extract()
        item['links'] = self.links_handler(all_links)
        yield item

    def redirect_handler(self, redirect, cur_url):
        # e.g. '0.5;url=http://helloworld.com'
        # e.g. '0.5;url=empty.exe'
        # after split, only need 'empty.exe'
        redirect_part = redirect
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
