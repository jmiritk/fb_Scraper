# -*- coding: utf-8 -*-
# TODO: read words from configuration.
'''For now it is hard coded. Unless a post has a "bad word" in it - we want it to be written to DB
This filters new  posts that were now scraped from HTML'''


class PostsFilter(object):
    def searchWord(self, posts):

        bad_words = []
        bad_posts = []
        good_posts = []
        good_words = []
        try:
            for post in posts:
                if any(sword in post['content'] for sword in good_words) or not any(sword in post['content'] for sword in bad_words):
                # #if word in post['content']:
                    print  'good  is in' + post['content']
                    good_posts.append(post)
                elif any(sword in post['content'] for sword in bad_words):
                    print  'bad word is in' + post['content']
                    bad_posts.append(post)

        except Exception as e:
            print 'error occured in words filter:' + e

        print 'finished words'
        return {'good_posts':good_posts,'bad_posts':bad_posts}