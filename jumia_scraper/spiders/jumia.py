import scrapy


class JumiaSpider(scrapy.Spider):
    name = 'jumia'
    start_urls = ['https://www.jumia.com.ng/kettles/']

    def parse(self, response):
        products =  response.css('article.prd._fb.col.c-prd')
        for product in products:
            name = product.css('a.core div.info h3.name::text').get()
            # name = product.xpath("//a[@class='core']/div[@class='info']/h3[@class='name']/text()").get()
            
            price = product.css('a.core div.info div.prc::text').get()
            # price = product.xpath("//a[@class='core']/div[@class='info']/div['prc']/text()").get()
            if price:
                price = price.replace('₦ ', '')
                if "-" in price:
                    _index = price.index(' -') 
                    price = price[_index:]
                else:
                    price = price
            else:
                price = '0'

            # rating = product.xpath("//a[@class='core']/div[@class='info']/div[@class='rev']/div/text()").get()
            rating = product.css('a.core div.info div.rev div::text').get()
            if rating:
                out_index = rating.index(' out')
                rating = rating[:out_index]
                
            else:
                rating = '0'
            
            # discount = product.xpath("//a[@class='core']/div[@class='info']/div[@class='s-prc-w']/div[@class='tag _dsct _sm']/text()").get()
            discount = product.css('a.core div.info div.s-prc-w div.tag._dsct._sm::text').get()
            if discount:
                discount = discount
                
            else:
                discount = '0%'

            if name is None:
                pass
            else:
                yield {
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'discount': discount,
                }

        next_page = response.css('a.pg::attr(href)').getall()[-2]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
