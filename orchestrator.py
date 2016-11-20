import sys

import userUi
from configuration import Configuration
from htmlProvider import HtmlProvider
from postsFilter import PostsFilter
from postsScraper import PostsScraper
from pyMongoHandler import PyMongoHandler


class Orchestrator(object):
    def __init__(self, configPath):
        self.setEncoding()
        self.config = Configuration(configPath).config
        self.dbHandler = PyMongoHandler(self.config)

    def orchestrate(self):
        #self.scrapePostsToDb()
        self.loadPostsFromDB()

    def scrapePostsToDb(self):

        html = HtmlProvider(self.config).getFbHtml()
        posts = PostsScraper().scrapePosts(html)
        sorted = PostsFilter().searchWord(posts)
        self.dbHandler.writeToDb(sorted)

    def loadPostsFromDB(self):
        while True:
            loadedPosts = self.dbHandler.loadFromDb()
            sorted = PostsFilter().searchWord(loadedPosts)
            userUi.createTable(sorted['good_posts'], self.dbHandler)
            #TODO: add close loop option

    # TODO: move elsewhere
    def setEncoding(self):
        reload(sys)
        sys.setdefaultencoding('utf8')
