# CSS selectors

next_page = response.css('a[title=Next]::attr(href)').get()
allproducts = response.css('div.product-item-info')
id = re.sub(re.compile(r'<span.*?>.*?</span>|<div.*?>|</div>'), '', response.css('div.sku-bg').get()).strip()
price = response.css('span.price::text').get()
link = response.css('a.product-item-link::attr(href)').get()
name = response.css('img.product-image-photo.image::attr(alt)').get()
rating = response.css('div.rating-result span span::text').get()