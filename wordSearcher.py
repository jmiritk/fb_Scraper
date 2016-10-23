'''Searches for a phrase given in configuration file:
 first inside the post and if it's not there - in the post comments'''

class WordSearcher(object):

    def __init__(self, config):
        self.word = config["search"]["phrase"]

    def searchWord(self, posts):
        word = self.word
        res = []
        for post in posts:
            if word in post['content']:
                print word + 'is in' + post['content']
                res.append(post)
            else:
                if self.searchInComments(post['comments']):
                    res.append(post)

            return res

    def searchInComments(self, comments):
            word = self.word
            for comment, replies in comments.items():
                if word in comment:
                    print comment + 'contains' + word
                    return True
