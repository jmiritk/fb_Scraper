import sys

import userUi
from configuration import Configuration
from htmlProvider import HtmlProvider
from postsFilter import PostsFilter
from postsScraper import PostsScraper
from pyMongoHandler import PyMongoHandler



class Orchestrator(object):
    #TODO: move elsewhere
    def setEncoding(self):
        reload(sys)
        sys.setdefaultencoding('utf8')

    def orchestrate(self, configPath):
        self.setEncoding()

        config = Configuration(configPath).config

        dbHandler = PyMongoHandler(config)
        print 'getting HTML'
        html = HtmlProvider(config).getFbHtml()

        print 'scraping posts'
        posts = PostsScraper().scrapePosts(html)

        print 'sorting posts'
        sorted = PostsFilter().searchWord(posts)

        print 'insert to db'
        dbHandler.writeToDb(sorted)
        while True:
            print 'loading from db'
            loadedPosts = dbHandler.loadFromDb()
            print 'printing to user'
            userUi.createTable(loadedPosts, dbHandler)

