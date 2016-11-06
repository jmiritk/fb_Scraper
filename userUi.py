
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import webbrowser

from PySide import  QtGui, QtCore

'''This class creates a table from the first 10 posts that it received.
 When overing over a post conent, the entire post is shown.
 If user marked post as irrelevant or sent, db will be updated accordingly upon Submit button pressed.
 When pressing on URL - the post will be open in Chrome new tab.
 If marked as sent and email was found, it will automatically send mail from the configured e-mail.'''

ROWS_IN_TABLE = 10
COLS_IN_TABLE = 6

class Window(QtGui.QWidget):
    def __init__(self, rows, columns, posts, dbHandler):

                QtGui.QWidget.__init__(self)
                self.wtable = QtGui.QTableWidget(rows, columns, self)
                self.posts = posts
                self.dbHandler = dbHandler
                self._irrelevant = []
                self._sent = []
                # TODO: read headers from file
                self.headers = ["content", "_id", "email", "irrelevant", "sent", "link"]

                for i in range(0, len(posts)):
                    self.createTableRow(i, posts[i])

                self.wtable.setHorizontalHeaderLabels(self.headers)
                self.wtable.setGeometry(0, 0, 800, 800)
                self.setGeometry(800, 800, 800, 800)
                self.setButtons()
                self.setWindowTitle('Job Posts')
                self.show()

    def setButtons(self):
        btn1 = QtGui.QPushButton("Submit", self)
        btn1.move(30, 500)
        btn2 = QtGui.QPushButton("Next Posts", self)
        btn2.move(150, 500)
        btn1.clicked.connect(self.submitClicked)
        # close table when looking for next posts and go back to orchestrator to continue loop
        # TODO: write better solution
        btn2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.wtable.itemClicked.connect(self.handleItemClicked)

    #TODO: split to smaller functions
    def createTableRow(self,row_num , post):
        content = QtGui.QTableWidgetItem(post['content'])
        content.setToolTip(post['content'].replace(".", "\n"))
        self.wtable.setItem(row_num, 0, content)

        id = QtGui.QTableWidgetItem(post['_id'])
        self.wtable.setItem(row_num, 1, id)

        link = QtGui.QTableWidgetItem("https://www.facebook.com/" + post['link'])
        self.wtable.setItem(row_num, 5, link)

        email_str = (None if 'email' not in post.keys() else post['email'])
        email = QtGui.QTableWidgetItem(email_str)
        self.wtable.setItem(row_num, 2, email)

        irrelevant = QtGui.QTableWidgetItem("")
        irrelevant.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        irrelevant.setCheckState(QtCore.Qt.Unchecked)
        self.wtable.setItem(row_num, 3, irrelevant)

        toSend = QtGui.QTableWidgetItem("")
        toSend.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        toSend.setCheckState(QtCore.Qt.Unchecked)
        self.wtable.setItem(row_num, 4, toSend)

    #send to db update instructions andrelvant post ids
    def submitClicked(self):
        self.dbHandler.updateIrrelevant(self._irrelevant)
        self.dbHandler.updateSent(self._sent)

    #determine action by  event type and column index
    def handleItemClicked(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            if item.column() == self.headers.index("irrelevant"):
                self._irrelevant.append(self.wtable.item(item.row(),  1).text())
            elif item.column() == item.column() == self.headers.index("sent"):
                self._sent.append(self.wtable.item(item.row(), 1).text())
        elif item.column() == self.headers.index("link"):
                webbrowser.open_new(self.wtable.item(item.row(), item.column()).text())

#TODO: find way to listen to event outside class
def createTable(posts, dbHandler):
    app = createApp()
    window = Window(ROWS_IN_TABLE, 6, posts[:ROWS_IN_TABLE], dbHandler)
    window.resize(800, 800)
    window.show()
    app.exec_()


# TODO: find proper Singleton replacement
# create QApplication if it doesnt exist
def createApp():
    app = QtGui.QApplication.instance()
    if not app:
        app = QtGui.QApplication(sys.argv)
    return app


