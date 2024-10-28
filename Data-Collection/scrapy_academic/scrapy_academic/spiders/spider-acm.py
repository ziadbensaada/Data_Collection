import scrapy
from scrapy_academic.items import AcademicItem
from urllib.parse import quote

class AcmSpider(scrapy.Spider):
    name = "academic"
    allowed_domains = ["dl.acm.org"]
    
    def __init__(self, query="machine learning", num_pages=5, *args, **kwargs):
        super(AcmSpider, self).__init__(*args, **kwargs)
        self.query = quote(query)
        self.num_pages = int(num_pages)
        self.start_urls = [f"https://dl.acm.org/action/doSearch?AllField={self.query}&language=fr"]

    def parse(self, response):
        articles = response.css('.issue-item.issue-item--search.clearfix')
        
        for article in articles:
            


            item = AcademicItem(
                journal=article.css('.epub-section__title::text').get(),
                doi=article.css('.issue-item__doi::text').get(),
                titre=article.css('.issue-item__title a::text').get(),  # Verify this selector
                chercheurs = ", ".join([name.css('a span::text').get() 
                for name in article.css('.hlFld-ContribAuthor')
                ]),
                abstract=article.css('.issue-item__abstract p::text').get(),
                date=response.css('.bookPubDate::attr(data-title)').get(),
            )
            yield item
        
        # Pagination
        next_page = response.css('a.pagination__btn--next::attr(href)').get()
        if next_page and self.num_pages > 1:
            self.num_pages -= 1
            yield response.follow(next_page, self.parse)
