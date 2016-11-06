# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re

'''Receives an html object and parse it into posts and their comments, using BeautifulSoup parsing library'''

class PostsScraper(object):
    # this method creates a list of posts
    def scrapePosts(self, raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        print 'got html'
        posts = []

        for itm in soup.find_all("div", class_="userContentWrapper"):
            print 'collecting...'
            post = self.collectPostInfo(itm)
            if post:
                posts.append(post)

        print 'total posts:' + str(len(posts))
        return posts

    # TODO: write more occurate selector
   # each post post is a dictionary
    def collectPostInfo(self, itm):
        post = {}
        #post['test'] = 'test1'
        post['content'] = self.getContent(itm.find("div", class_="userContent"))
        post['date'] = itm.find("abbr")['data-utime']
        post['user_name'] = itm.find("span", class_="fwb").getText()
        post['link'] = itm.find("a", href=re.compile('^/groups'))["href"]
        post['likes_amount'] = self.determineLikesAmount(itm)
        post['_id'] = post['date'] + "_" + post['user_name']
        mail = self.fineEmail(post['content'])
        if mail:
         post['email'] = self.fineEmail(post['content'])
        #post['comments'] = self.getAllComments(itm)
        return post

    def fineEmail(self, str):
        #TODO: add creadit for regex
        regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                            "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                            "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
        mail = re.search(regex, str)
        if mail:
            return mail.group(0)




    def getContent(self,itm):
        raw_contetnt = itm.findChildren()
        textContent = ""
        for childContent in raw_contetnt:
            textContent += childContent.getText()
        return textContent


    def determineLikesAmount(self, itm):
        amount = itm.find("span", class_="_4arz")
        if amount:
            return amount.getText()
        else:
            return 0


    #This return a dictionary where a comment on post is the key, and a list of replies to comment is the value )if exists)
    def getAllComments(self, itm):
        comments = itm.find_all("div", class_="UFIRow")
        commentsDic = {}
        for comment in comments:
            replies = comment.find_next_sibling()

            if self.checkIfRepliesExist(replies):
                commentsDic[self.getCommentText(comment)] = self.getRepliesText(replies)
            else:
                commentsDic[comment] = None
        return commentsDic


    def checkIfRepliesExist(self, replies):
        return replies and len(replies) > 1 and replies.get("class")[1] == "UFIReplyList"


    def getRepliesText(self, replies_raw):
        replies = replies_raw.find_all("div", class_="UFIComment")
        repsTxt = []
        for reply in replies:
            repsTxt.append(self.getCommentText(reply))
        return repsTxt


    def getCommentText(self, itm):
        return itm.find("span", class_="UFICommentBody").getText()
