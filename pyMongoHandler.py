
# -*- coding: utf-8 -*-
from pymongo import MongoClient

import FBScraper.cvMailSender as sender


class PyMongoHandler(object):
    def __init__(self, config):
       self.collection_name = config["collection_name"]
       self.db = self.createDB()

    #Insert post db if not already exists.
    def insertToDB(self, posts, collection):
        try:
            for post in posts:
                print 'looking...'
                res = collection.find({"_id": post["_id"]})
                if len(list(res)) is 0:
                    print 'inserting...'
                    collection.insert_one(post)
        except Exception as e:
            print e
        print 'finished'

    def createDB(self):
        try:
            client = MongoClient('localhost:27017')
            #TODO: get db name from parameter
            return client.MainDB

        except Exception as e:
            print(e)


    def loadFromDb(self):
        db = self.db
        return list(db[self.collection_name].find({"irrelevant": {"$exists": False}, "sent": {"$exists": False}, "link": {"$regex": ".*wwci.*"}}))


    #write new and relevant posts to DB
    #filtered as irrelevant posts go to 'bad posts db'
    def writeToDb(self, posts):
        self.insertToDB(posts["good_posts"],self.db)
        self.insertToDB(posts["bad_posts"], self.db)

    #TODO: merge methods
    #if user marked post as irrelevant - ignore, later on - a routine cleaning will be added
    def updateIrrelevant(self, posts):
        #TODO: remove create db, find nicer loop
        db = self.db
        res = []
        for p in posts:
            val1 = db[self.collection_name].find({"_id": p})
            res.append(val1)
            db[self.collection_name].update({"_id": p}, {"$set": {"irrelevant": "True"}}, True)

        print 'updated irrelevant'

    '''when user updated this job as relevant, and we recognized email, auto send mail.
    otherwise - assume the user sent it himself and simply update DB'''
    def updateSent(self,posts):
        #TODO: write nicer loop
        db = self.db
        posts = []
        for p in posts:
            posts = db[self.collection_name].find({"_id": p})
            posts.append(posts)
            post = list(posts)
            if('email'  in post[0].keys()):
                mail = post[0]["email"]
                print 'sending ' +mail
                sender.handleMail(mail)
            db[self.collection_name].update({"_id": p}, {"$set": {"sent": "True"}}, True)

        print 'updated sent'
