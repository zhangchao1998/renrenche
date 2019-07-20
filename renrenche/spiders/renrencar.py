# -*- coding: utf-8 -*-
import scrapy
from renrenche.items import RenrencheItem


class RenrencarSpider(scrapy.Spider):
    name = 'renrencar'
    allowed_domains = ['renrenche.com']
    start_urls = []
    with open('数据.txt', 'r') as f:
        all_url = f.readlines()
    for i in all_url:
        start_urls.append(i[0:-1])

    def parse(self, response):
        page_car = response.xpath('//ul[@class="row-fluid list-row js-car-list"][1]/li/a[@rrc-event-param="search"]/@href').extract()
        for i in page_car:
            if not i.startswith('/car'):
                url = 'https://www.renrenche.com'+i
                yield scrapy.Request(url=url, callback=self.parse1,meta={'url':url},dont_filter=False)

    def parse1(self, response):
        name = response.xpath('//div[@class="right-container"]/div[@class="title"]/h1/text()').extract()[1]
        while name.endswith('\n') or name.endswith(' '):
            name = name[:-1]
        price = response.xpath('//div[@class="middle-content"]/div[@class="list price-list"]/p[@class="price detail-title-right-tagP"]/text()').extract()[0]
        mileage = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[1]/div/p/strong/text()').extract()[0]
        register_time = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[@class="span7"]/div/p/strong/text()').extract()[0]
        address = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[@class="span5 last car-licensed-city"]/div/p/strong/text()').extract()[0]
        standard = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[@class="span5 car-fluid-standard"]/div/p/strong/text()').extract()[0]
        gearbox = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[5]/div/p/strong/text()').extract()[0]
        transfer_record = response.xpath('//div[@class="row-fluid-wrapper"]/ul/li[@class="car-transfer"]/p/strong/text()').extract()[0]
        car_link = response.meta['url']
        item = RenrencheItem()
        item['name'] = name
        item['price'] = price
        item['mileage'] = mileage
        item['register_time'] = register_time
        item['address'] = address
        item['standard'] = standard
        item['gearbox'] = gearbox
        item['transfer_record'] = transfer_record
        item['car_link'] = car_link
        yield item
