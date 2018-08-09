import scrapy
from link_spider.items import ListingItem

class ListingsSpider(scrapy.Spider):
    name = 'link_spider'


    def start_requests(self):
        first = 'https://www.glassdoor.nl/Vacature/amsterdam-software-developer-vacatures-SRCH_IL.0,9_IC3064478_KO10,28.htm'

        def get_urls(url):
            urls = []
            for x in range(0,50):
                urr = url[:-4] + '_IP' + str(x) + '.htm'
                urls.append(urr)
            return urls

        urlss = []
        urlss = get_urls(first)

        urls = urlss
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        result = response.css("li.jl > div:nth-child(2)")
        next = response.xpath("//*[@id='FooterPageNav']/div/ul/li[7]/a")


        for listing in result:
            title = listing.css("div:nth-child(1)>div:nth-child(1)>a::text").extract_first()
            company1 = listing.css("div:nth-child(2)>div:nth-child(1)::text").extract_first()
            city = listing.css("div:nth-child(2)>div:nth-child(1) > span::text").extract_first()
            link1 = listing.css("div:nth-child(1)>div:nth-child(1)>a::attr(href)").extract_first()
            link = 'https://www.glassdoor.nl' + link1
            company = company1[1:-3]
            listingItem = ListingItem()

            listingItem['title'] = title
            listingItem['company'] = company
            listingItem['link'] = link
            listingItem['city'] = city

            yield listingItem
