from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import logging
import re
class MyItem(Item):
    url= Field()


class someSpider(CrawlSpider):
    allowed_domains = ['DOMAIN']
    start_urls = ['URL']
    regex_output = "REGEX-TO-EXTRACT-DOMAINS/URLS"
    name = 'crawltest'
    rules = (Rule(LxmlLinkExtractor(allow=(),deny = (),deny_extensions=None,tags=('a','area','q','meta','track','object','style','video','applet','body','button','del','head','html','input','ins','img','source','base','blockquote','embed','form','frame','iframe','link','script'), attrs=('href','src','data','archive','codebase','poster','code','cite','background','formaction','profile','xmlns','ping','longdesc','srcset','action','srcdoc','scheme'), process_value=None, unique=True), callback='parse_obj', follow=True),)
    def parse_obj(self,response):
        item = MyItem()
        item['url'] = []
        for link in LxmlLinkExtractor(allow=(),deny = (),deny_extensions=None ,tags=('a','area','q','meta','track','object','style','video','applet','body','button','del','head','html','input','ins','img','source','base','blockquote','embed','form','frame','iframe','link','script'), attrs=('href','src','data','archive','codebase','poster','code','cite','background','formaction','profile','xmlns','ping','longdesc','srcset','action','srcdoc','scheme'), process_value=None, unique=True).extract_links(response):
            is_allowed=False
            is_regex_output = False
            for allowed_domain in self.allowed_domains:
                if re.match("^https?:\/\/"+allowed_domain, link.url) is not None:
                    is_allowed = True
            if re.match("^https?:\/\/"+self.regex_output, link.url) is not None:
                is_regex_output = True
            if is_allowed:
                item['url'].append(link.url)
            if is_regex_output:
                z = open("re-match-urls.txt","a")
                z.write(link.url+"\n")
                z.close()
            else:
                f = open("other-urls.txt","a")
                f.write(link.url+"\n")
                f.close()
        return item

if __name__ == "__main__":
    print("Starting scrapy")
    configure_logging(install_root_handler=True)
    logging.disable(10)  # DEBUG = 10
    print("Starting crawling process")
    process = CrawlerProcess()
    process.crawl(someSpider)
    process.start()
