from decimal import Decimal
from ebay.models import Product, Projection

import scrapy
import json

class ecrawlSpider(scrapy.Spider):
    name = 'ecrawl'
    def __init__(self, rows=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.rows = json.loads(rows)

    def start_requests(self):
        for row in self.rows:
            base_URL = 'https://www.ebay.com/sch/'
            keywords = '?_nkw=' + row['name'].replace(' ', '%20') # added URL encoding
            free_shipping = '&LH_FS=1'
            best_match = '&_sop=12'
            # Completed_Listings = '&LH_Complete=1'
            # Items_Sold = '&LH_Sold=1'
            # Search_Description = '&LH_TitleDesc=1'
            # New_condition = '&LH_ItemCondition=11'

            search_URL = base_URL + keywords + free_shipping + best_match

            urls = [search_URL]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse_listing_page,
                meta={'name': row['name'], 'price': row['wholesale_price'], 'weight': row['wholesale_weight'], 'fee': row['wholesale_fee']})

    # follows listing link from search results
    def parse_listing_page(self, response):
        product_page = response.css('#mainContent .s-item__link::attr(href)').extract_first()
        if product_page:
            yield scrapy.Request(product_page, callback=self.parse_dir_page,
            meta={'name': response.meta['name'], 'price': response.meta['price'], 'weight': response.meta['weight'], 'fee': response.meta['fee']})

    # Extracts data on listing page and save to list.csv
    def parse_dir_page(self, response):
        name = response.css('#itemTitle::text').extract()[0]
        price = Decimal(response.css('#prcIsum::text').extract()[0].lstrip('\n\t\t\t\t\t\t\t\t\t\tUS $')) if response.css('#prcIsum::text') else 'NA'
        # Shipping = 1 if response.css('#fshippingCost span::text') else 0
        sold = response.css('.vi-qty-pur-lnk *::text').extract()[1].lstrip() if response.css('.vi-qty-pur-lnk *::text') else 0
        updates = response.css('#vi_notification_new span::text').extract()[0] if response.css('#vi_notification_new span::text') else 'NA'

        wholesale_price = Decimal(response.meta['price'])
        fee = Decimal(response.meta['fee'])
        weight = Decimal(response.meta['weight'])

        # calculte profit
        if weight < 6:
            fee += Decimal(2.66)
        elif weight < 12:
            fee += Decimal(3.56)
        elif weight < 16:
            fee += Decimal(3.86)
        else:
            fee += Decimal(5.36)

        profit = price - wholesale_price - fee
        profit_percentage = profit/wholesale_price

        image = response.css('#icImg::attr(src)').extract()[0]

        product = Product()
        product.url = response.url
        product.ebay_name = name
        product.name = response.meta['name']
        product.wholesale_price = wholesale_price
        product.retail_price = price
        product.profit = profit
        product.profit_percentage = Decimal('{0:.2f}'.format(profit_percentage))
        product.wholesale_weight = weight
        product.wholesale_fee = fee
        product.units_sold = sold
        product.updates = updates
        product.image = image
        product.save()

        # follows purchase link from product page
        purchase_page = response.css('.vi-pop-drkgry::attr(href)').extract_first()
        purchase_page_hot = response.css('.vi-qtyS-hot-red > a::attr(href)').extract_first()
        if purchase_page:
            yield scrapy.Request(purchase_page, callback=self.parse_purchase_page, meta={'name': name})
        if purchase_page_hot:
            yield scrapy.Request(purchase_page_hot, callback=self.parse_purchase_page, meta={'name': name})

    def parse_purchase_page(self, response):
        purchase_price = response.css('tr td:nth-last-child(4)::text').extract()    #.lstrip('US $')
        purchase_quantity = response.css('tr td:nth-last-child(3)::text').extract()
        purchase_date = response.css('tr td:nth-last-child(2)::text').extract()[:-9]

        for (price, quantity, date) in zip(reversed(purchase_price), reversed(purchase_quantity), reversed(purchase_date)):
            projection = Projection()
            projection.purchase_name = response.meta['name']
            projection.purchase_price = price
            projection.purchase_quantity = int(quantity)
            projection.purchase_date = date
            projection.save()
