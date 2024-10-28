import scrapy
from iee.items import IeeItem
from scrapy_splash import SplashRequest

class IeeSpider(scrapy.Spider):
    name = "iee"
    topic = "None"

    ITEM_PIPELINES = {
        'myproject.pipelines.PricePipeline': 100,
        'myproject.pipelines.JsonWriterPipeline': 800,
    }

    def __init__(self, keywords=None, topic=None, *args, **kwargs):
        super(IeeSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=%s' % keywords]
        self.topic = topic

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 3})

    def parse(self, response):
        # Loop through each article link
        for article in response.css('a::attr(href)'):
            article_url = article.extract()

            # Skip invalid links (like "javascript:history.back();")
            if article_url.startswith('javascript') or 'history.back' in article_url:
                continue

            # Complete relative URLs (if necessary)
            if article_url.startswith('/'):
                article_url = 'https://ieeexplore.ieee.org' + article_url

            # Ensure it's a valid URL before proceeding
            if 'http' in article_url:
                yield SplashRequest(article_url, self.parse_article, args={'wait': 3})

        # Follow next page links (if pagination exists)
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield SplashRequest(next_page_url, self.parse, args={'wait': 3})

    def parse_article(self, response):
        item = IeeItem()

        # Extracting the article's details
        title = response.css('.document-title').css('span::text').extract_first()

        authors = response.css('.authors-info').css('span').css('a').css('span.LexL').extract()

        affiliation_name = response.css('.affiliation-name::text').extract_first() if response.css('.affiliation-name::text').extract_first() else ""
        affiliation_city = response.css('.affiliation_city::text').extract_first() if response.css('.affiliation_city::text').extract_first() else ""
        affiliation_country = response.css('.affiliation_country::text').extract_first() if response.css('.affiliation_country::text').extract_first() else "USA"

        abstract = response.css('.abstract-desktop div.sections').css('div::text').extract()

        location = response.css('.dot-location-conference').css('text').extract()
        pub_year = response.css('.stats-document-abstract-publishedIn').css('a::text').extract()

        item['title'] = title
        item['authors'] = ', '.join(authors)
        item['abstract'] = ' '.join(abstract)
        item['location'] = ', '.join(location.extract())
        item['date_pub'] = pub_year[0].split(' ')[0] if pub_year else 'Unknown'
        item['topic'] = self.topic
        item['latitude'] = 0
        item['longitude'] = 0
        item['journal'] = ' '.join(pub_year[0].split(' ')[1:]) if pub_year else 'Unknown'

        yield item
