import scrapy
from link_spider.items import ListingItem
from w3lib.html import remove_tags

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

        urls = get_urls(first)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        result = response.css("li.jl > div:nth-child(2)")
        for listing in result:
            title = listing.css("div:nth-child(1)>div:nth-child(1)>a::text").extract_first()
            link1 = listing.css("div:nth-child(1)>div:nth-child(1)>a::attr(href)").extract_first()
            link = 'https://www.glassdoor.nl' + link1
            relevant = ['front', 'Front', 'Frontend', 'Fullstack', 'Junior', 'Software']
            if any(x in title for x in relevant):
                yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        extr = response.css('div.jobDescriptionContent').extract_first()
        result = remove_tags(extr)
        listingItem = ListingItem()

        listingItem['posted'] = response.xpath('//*[@id="HeroHeaderModule"]/div[3]/div[2]/div[2]/span/text()').extract_first()[1:3]
        listingItem['link'] = response.url
        listingItem['title'] = response.xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[2]/div[1]/h2/text()').extract_first()
        listingItem['company'] = response.xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[2]/span[2]/text()').extract_first()[1:]
        listingItem['city']= response.xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[2]/span[3]/text()').extract_first()
        listingItem['description'] = result

        react = ['react', 'React']
        if any(x in result for x in react):
            yield listingItem
