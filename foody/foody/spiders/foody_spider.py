# -*- coding: utf-8 -*-
import scrapy
import requests
from ..items import FoodyItem, ItemImage, ItemComments
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FoodySpiderSpider(scrapy.Spider):
    name = 'foody'
    allowed_domains = [
        "www.foody.vn"
    ]
    start_urls = [
        'http://www.foody.vn/ho-chi-minh/food/dia-diem?q='
    ]

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument('disable-infobars')
        self.driver = webdriver.Chrome(
            chrome_options=options, executable_path=r'/home/giacat/Documents/Foody_data/chromedriver_linux64/chromedriver')
        self.driver.get(
            "https://id.foody.vn/account/login?returnUrl=https://www.foody.vn/ho-chi-minh/food/dia-diem?q=")
        username = self.driver.find_element_by_id("Email")
        username.clear()
        username.send_keys("duysimple98")
        pwd = self.driver.find_element_by_id('Password')
        pwd.clear()
        pwd.send_keys('thanhduy66')
        self.driver.find_element_by_id('bt_submit').click()

        self.driver.implicitly_wait(30)

    def parse(self, response):
        self.driver.get(response.url)
        # hit = 0
        # while True and hit <= 5:
        #     view_more_button = WebDriverWait(self.driver, 30).until(
        #         EC.element_to_be_clickable((By.XPATH, '//*[(@id = "scrollLoadingPage")]//a')))
        #     view_more_button.click()
        #     time.sleep(2)
        #     hit += 1

        snode_foodys = response.css('h2 a')
        for i in snode_foodys:
            res_url = ('https://www.foody.vn%s' %
                       i.xpath('@href').extract_first())
            if('thuong-hieu' not in res_url):
                yield scrapy.Request(res_url, callback=self.parse_item)
            else:
                yield scrapy.Request(res_url, callback=self.parse_thuong_hieu)

    def parse_thuong_hieu(self, response):
        snode_ths = response.css('h2 a')
        for i in snode_ths:
            res_url = ('https://www.foody.vn%s' %
                       i.xpath('@href').extract_first())
            yield scrapy.Request(res_url, callback=self.parse_item)

    def parse_item(self, response):
        items = FoodyItem()
        itemimg = ItemImage()
        itemcmt = ItemComments()
        r = response.url
        items['url'] = r

        rq = requests.get(r)
        body = rq.text
        soup = BeautifulSoup(body, features="lxml")

        title = soup.find('h1', {'itemprop': 'name'}).text
        items['title'] = title

        if soup.find('img', {'class': 'pic-place'}) == None:
            pass
        else:
            cover_url = soup.find('img', {'class': 'pic-place'}).attrs
            items['coverurl'] = cover_url['src']

        category = soup.find('div', {'class': 'category-items'}).text
        items['category'] = category.replace('\n', '')

        if soup.find('div', {'itemprop': 'ratingValue'}) == None:
            pass
        else:
            avgscore = soup.find('div', {'itemprop': 'ratingValue'}).text
            items['avgscore'] = float(avgscore)

        addr = soup.find('span', {'itemprop': 'streetAddress'}).text
        items['address'] = addr

        dist = soup.find('span', {'itemprop': 'addressLocality'}).text
        items['district'] = dist

        city = soup.find('span', {'itemprop': 'addressRegion'}).text
        items['city'] = city

        lat = soup.find('meta', {'itemprop': 'latitude'}).attrs
        items['latitude'] = lat['content']

        lon = soup.find('meta', {'itemprop': 'longitude'}).attrs
        items['longitude'] = lon['content']

        t = soup.find('div', {'class': 'micro-timesopen'})
        op = t.find('span', {'class': ''}).text
        items['timeopen'] = op

        price = soup.find('span', {'itemprop': 'priceRange'})
        p = price.find('span', {'class': ''})
        items['pricerange'] = p.text

        yield items

        img_box = soup.find('div', {'class': 'microsite-box-content'})
        itags = img_box.find_all('img', {'class': ''})
        for i in itags:
            itemimg['url'] = r
            itemimg['imgurl'] = i['src']
            yield itemimg

        cmt_box = soup.find('div', {'class': 'foody-box-review'})
        ctags = cmt_box.find_all('li', {'class': 'review-item'})
        for c in ctags:
            itemcmt['url'] = r

            user = c.find('a', {'class': 'ru-username'}).text
            itemcmt['user'] = user.replace('\n', '')

            cmt_t = c.find('span', {'class': 'ru-time'}).text
            # convert_t = datetime.strptime(cmt_t.replace(',' , ''), '%d/%m/%Y %H:%M:%S')
            itemcmt['date'] = cmt_t

            if c.find('span', {'itemprop': 'reviewBody'}) == None:
                pass
            else:
                cont = c.find('span', {'itemprop': 'reviewBody'}).text
                itemcmt['content'] = cont
            yield itemcmt

    # def parse_item_img(self, response):
    #     r = response.url
