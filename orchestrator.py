from beautySoupScraper import BeautySoupScraper
from wordSearcher import WordSearcher
from configuration import Configuration
from seleniumHtmlProvider import SeleniumHtmlProvider
import sys


class Orchestrator(object):

    def setEncoding(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    def orchestrate(self):
        self.setEncoding()
        config = Configuration(sys.argv.pop(1)).config
        provider = SeleniumHtmlProvider(config).getFbHtml()
        html = provider
        posts = BeautySoupScraper().scrapePosts(html)
        # TODO: handle res
        res = WordSearcher(config).searchWord(posts)


Orchestrator().orchestrate()
