import scrapy
import re

class RugsSpider(scrapy.Spider):
    name = "rugs"
    allowed_domains = ["www.therugshopuk.co.uk"]
    start_urls = ["https://www.therugshopuk.co.uk/made-to-measure-rugs.html"]

    def parse(self, response):
        for item in response.css('div.product-item-info'):
            yield {
                'id': re.search(r'ID\s*:\s*(\w+)', re.sub(r'<.*?>', '', response.css('div.sku-bg').get()).strip()).group(1),
                'name': item.css('img.product-image-photo.image::attr(alt)').get(),
                'rating': item.css('div.rating-result span span::text').get(),
                'price': item.css('span.price::text').get(),
                'link': item.css('a.product-item-link::attr(href)').get() 
            }
            
        next_page = response.css('a[title=Next]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)