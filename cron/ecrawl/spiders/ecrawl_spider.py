from decimal import Decimal
from ebay.models import Product, Projection

import scrapy

class ecrawlSpider(scrapy.Spider):
    name = 'ecrawl'

    def start_requests(self):
        links = Product.objects.values('url')
        for link in links:
            yield scrapy.Request(link.get('url'), callback=self.parse_dir_page)

    # Extracts data on listing page and save to list.csv
    def parse_dir_page(self, response):
        name = response.css('#itemTitle::text').extract()[0]
        price = Decimal(response.css('#prcIsum::text').extract()[0].lstrip('\n\t\t\t\t\t\t\t\t\t\tUS $')) if response.css('#prcIsum::text') else 'NA'
        # Shipping = 1 if response.css('#fshippingCost span::text') else 0
        sold = response.css('.vi-qty-pur-lnk *::text').extract()[1].lstrip() if response.css('.vi-qty-pur-lnk *::text') else 0
        updates = response.css('#vi_notification_new span::text').extract()[0] if response.css('#vi_notification_new span::text') else 'NA'

        product = Product.objects.get(url=response.url)

        # update prices
        # if (Product.objects.values_list('retail_price', flat=True).get(url=response.url) != price):
        #     wholesale_price = Product.objects.values_list('wholesale_price', flat=True).get(url=response.url)
        #     fee = Product.objects.values_list('wholesale_fee', flat=True).get(url=response.url)
        #     weight = Product.objects.values_list('wholesale_weight', flat=True).get(url=response.url)

        #     # calculte profit
        #     if weight < 6:
        #         fee += Decimal(2.66)
        #     elif weight < 12:
        #         fee += Decimal(3.56)
        #     elif weight < 16:
        #         fee += Decimal(3.86)
        #     else:
        #         fee += Decimal(5.36)

        #     profit = price - wholesale_price - fee
        #     profit_percentage = profit/wholesale_price
        #     product.retail_price = price
        #     product.profit = profit
        #     product.profit_percentage = Decimal('{0:.2f}'.format(profit_percentage))

        # image = response.css('#icImg::attr(src)').extract()[0]

        # product.ebay_name = name
        # product.image = image
        product.units_sold = sold
        product.updates = updates
        product.save()

        # follows purchase link from product page
        purchase_page = response.css('.vi-pop-drkgry::attr(href)').extract_first()
        purchase_page_hot = response.css('.vi-qtyS-hot-red > a::attr(href)').extract_first()
        if purchase_page:
            yield scrapy.Request(purchase_page, callback=self.parse_purchase_page, meta={'name': name})
        if purchase_page_hot:
            yield scrapy.Request(purchase_page_hot, callback=self.parse_purchase_page, meta={'name': name})

    def parse_purchase_page(self, response):
        name = response.meta['name']
        purchase_price = response.css('tr td:nth-last-child(4)::text').extract()    #.lstrip('US $')
        purchase_quantity = response.css('tr td:nth-last-child(3)::text').extract()
        purchase_date = response.css('tr td:nth-last-child(2)::text').extract()[:-9]
        projection_exists = Projection.objects.filter(purchase_name=name).values('purchase_date').last()

        # filter out existing projection data
        latest_date = purchase_date[:purchase_date.index(projection_exists.get('purchase_date'))] if projection_exists else purchase_date

        for (price, quantity, date) in zip(reversed(purchase_price), reversed(purchase_quantity), reversed(latest_date)):
            projection = Projection()
            projection.purchase_name = name
            projection.purchase_price = price
            projection.purchase_quantity = int(quantity)
            projection.purchase_date = date
            projection.save()

