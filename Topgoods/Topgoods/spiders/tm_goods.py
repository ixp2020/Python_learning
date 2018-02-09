# -*- coding: utf-8 -*-

import scrapy
from Topgoods.items import TopgoodsItem

class TmGoodsSpider(scrapy.Spider):
    name = 'tm_goods'
    allowed_domains = ['http://www.tmall.com','list.tmall.com']
    start_urls = ['https://list.tmall.com/search_product.htm?spm=a220m.1000858.1000724.4.297277dbMgbgVm&cat=50025135&q=2017%D0%C2&sort=d&style=g&search_condition=4&from=sn_1_prop&active=1&industryCatId=50025135#J_Filter']
    count = 0

    def parse(self, response):
        TmGoodsSpider.count += 1

        divs = response.xpath("//div[@id='J_ItemList']/div[@class='product  ']/div")
        #divs = response.xpath("//div[@id='J_ItemList']/div")
        # print '---------------------------'
        # print len(divs)
        # #print divs
        # print '---------------------------'
        if not divs:
            self.log("list page error--%s"%response.url)
        for div in divs:
            item=TopgoodsItem()
            item['GOODS_PRICE'] = div.xpath("p[@class='productPrice']/em/@title")[0].extract()
            item['GOODS_NAME'] = div.xpath("p[@class='productTitle']/a/@title")[0].extract()
            pre_goods_url = div.xpath("p[@class='productTitle']/a/@href")[0].extract()
            item['GOODS_URL'] = pre_goods_url if "http:" in pre_goods_url else ("http:"+pre_goods_url)

            yield scrapy.Request(url=item["GOODS_URL"],meta={'item':item},callback=self.parse_detail,
                                 dont_filter=TabError)

    def parse_detail(self,respone):
        div = respone.xpath('//div[@class="extend"]/ul')
        if not div:
            self.log("Detail Page error--%s"%respone.url)
        item = respone.meta['item']
        div= div[0]
        item['SHOP_NAME'] = div.xpath("li[1]/div/a/text()")[0].extract()
        item['SHOP_URL'] = div.xpath("li[1]/div/a/@href")[0].extract()
        item['COMPANY_NAME'] = div.xpath("li[3]/div/text()")[0].extract().strip()
        item['COMPANY_ADDRESS'] = div.xpath("li[4]/div/text()")[0].extract().strip()

        yield item