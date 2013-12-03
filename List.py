# -*- coding: utf-8 -*-

import re
import sys
import urllib
import sqlite3
import webbrowser
from dbwrite import dbwrite
from pyquery import PyQuery as pq
from PyQt4 import QtCore, QtGui
from download import DownloadTab
from anime_commands import *


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(SearchTab(), u"搜索")
        tabWidget.addTab(DownloadTab(), u"下载")
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)

        self.setLayout(mainLayout)
        self.setWindowTitle(u"极影动漫下载")
        self.setWindowIcon(QtGui.QIcon('dango.ico'))
        self.resize(800, 400)


class SearchTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SearchTab, self).__init__(parent)
        self.res = []
        self.worker = Worker()
        self.connect(self.worker, QtCore.SIGNAL('resultReady'), self.showAnimes)
        self.list = read('List.dat')
        self.listText = []
        for line in self.list:
            self.listText.append(' '.join(line))

        deleteListButton = self.createButton(u"&删除", self.deleteList)
        addListButton = self.createButton(u"&保存条目", self.addList)
        #downloadButton = self.createButton(u"&下载", self.download)
        searchButton = self.createButton(u"&搜索", self.search)
        dbreadButton = self.createButton(u"&读取数据库", self.dbread)
        dbwriteButton = self.createButton(u"&写入数据库", self.dbwrite)
        dbdeleteButton = self.createButton(u"&删除条目", self.dbdelete)

        self.animeTitle, self.searchName, self.subTeams = read('AnimeInfo.dat')
        self.listComboBox = self.createComboBox(self.listText, self.updateComboBoxs)
        self.listComboBox.setEditable(False)
        self.titleComboBox = self.createComboBox(self.animeTitle, self.updateSubTeamComboBox)
        self.subTeamComboBox = self.createComboBox([u'请先选择动漫'])
        self.subComboBox = self.createComboBox([u'', u'GB', u'BIG', u'简', u'繁', u'繁體', u'簡繁'])
        self.HDComboBox = self.createComboBox([u'', u'720P', u'480P', u'1080P'])
        self.userComboBox = QtGui.QLineEdit()

        self.animeTable = self.createTable()

        # self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        subLabel = QtGui.QLabel(u" 字体:")
        HDLabel = QtGui.QLabel(u" 清晰度:")
        userLabel = QtGui.QLabel(u"其他关键字:")
        self.animesFoundLabel = QtGui.QLabel()

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(dbreadButton)
        buttonsLayout.addWidget(dbwriteButton)
        buttonsLayout.addWidget(dbdeleteButton)
        # buttonsLayout.addWidget(downloadButton)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.listComboBox, 0, 0, 1, 6)
        mainLayout.addWidget(deleteListButton, 0, 6, 1, 2)
        mainLayout.addWidget(self.titleComboBox, 1, 0, 1, 4)
        mainLayout.addWidget(self.subTeamComboBox, 1, 4, 1, 2)
        mainLayout.addWidget(searchButton, 1, 6, 1, 1)
        mainLayout.addWidget(addListButton, 1, 7, 1, 1)
        mainLayout.addWidget(subLabel, 2, 0, 1, 1)
        mainLayout.addWidget(self.subComboBox, 2, 1, 1, 1)
        mainLayout.addWidget(HDLabel, 2, 2, 1, 1)
        mainLayout.addWidget(self.HDComboBox, 2, 3, 1, 1)
        mainLayout.addWidget(userLabel, 2, 4, 1, 1)
        mainLayout.addWidget(self.userComboBox, 2, 5, 1, 3)
        mainLayout.addWidget(self.animeTable, 3, 0, 1, 8)
        mainLayout.addWidget(self.animesFoundLabel, 4, 0, 1, 0)

        mainLayout.addLayout(buttonsLayout, 5, 5, 1, 3)
        self.setLayout(mainLayout)

    def download(self):
        for Range in self.animeTable.selectedRanges():
            for i in self.res[Range.topRow():Range.bottomRow() + 1]:
                print i[2]

    def dbwrite(self):
        dbwrite(self.res)

    def dbdelete(self):
        cx = sqlite3.connect("ktxp.db")
        cx.isolation_level = None
        cx.text_factory = str
        cu = cx.cursor()
        index = []
        for Range in self.animeTable.selectedRanges():
            for i in range(Range.topRow(), Range.bottomRow() + 1):
                index.append(i)
                cu.execute("DELETE FROM anime_table WHERE title=?", (self.res[i]['title'],))
        cx.commit()
        cu.close()
        cx.close()
        index.sort(reverse=True)
        for i in index:
            print i
            self.animeTable.removeRow(i)

    def updateSubTeamComboBox(self):
        self.subTeamComboBox.clear()
        try:
            index = self.titleComboBox.currentIndex()
        except:
            index = 0
        self.subTeamComboBox.addItems(self.subTeams[index].keys())

    def updateComboBoxs(self):
        title, subTeam, sub, HD, user = self.list[self.listComboBox.currentIndex()]
        self.titleComboBox.setEditText(title)
        self.updateSubTeamComboBox()
        self.subTeamComboBox.setEditText(subTeam)
        self.subComboBox.setEditText(sub)
        self.HDComboBox.setEditText(HD)
        self.userComboBox.setText(user)

    def addList(self):
        self.list.insert(0, [unicode(self.titleComboBox.currentText()), unicode(self.subTeamComboBox.currentText()),
                             unicode(self.subComboBox.currentText()), unicode(self.HDComboBox.currentText()),
                             unicode(self.userComboBox.text())])
        self.listText.insert(0, u' '.join(self.list[0]))
        self.listComboBox.insertItem(0, self.listText[0])
        self.listComboBox.setCurrentIndex(0)
        self.writeList()

    def deleteList(self):
        index = self.listComboBox.currentIndex()
        del (self.list[index])
        del (self.listText[index])
        self.listComboBox.removeItem(index)
        self.writeList()

    def search(self):
        if self.worker.isRunning():
            if self.questionMessage():
                self.worker.exit()
            else:
                return
        title = unicode(self.titleComboBox.currentText())
        try:
            title = self.searchName[self.animeTitle.index(title)]
        except Exception, e:
            print e
        keywords = u' '.join(
            [title, unicode(self.subTeamComboBox.currentText()), unicode(self.subComboBox.currentText()),
             unicode(self.HDComboBox.currentText()), unicode(self.userComboBox.text())])
        #print keywords
        self.worker.setKeywords(keywords)
        self.worker.start()
        self.animesFoundLabel.setText(u"正在更新列表...")

    def dbread(self):
        cx = sqlite3.connect("ktxp.db")
        cx.isolation_level = None
        cx.text_factory = str
        cx.row_factory = sqlite3.Row
        cu = cx.cursor()
        cu.execute("SELECT * FROM anime_table ORDER BY subTime DESC")
        res = cu.fetchall()
        cu.close()
        cx.close()

        self.showAnimes(res)

    def showAnimes(self, res):
        self.res = res
        self.animeTable.setRowCount(0)
        self.animeTable.clearContents()
        for l in res:
            timeItem = QtGui.QTableWidgetItem(l['time'])
            timeItem.setFlags(timeItem.flags() ^ QtCore.Qt.ItemIsEditable)
            titleItem = QtGui.QTableWidgetItem(l['title'].decode('utf-8'))
            titleItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.animeTable.rowCount()
            self.animeTable.insertRow(row)
            self.animeTable.setItem(row, 0, timeItem)
            self.animeTable.setItem(row, 1, titleItem)

        self.animesFoundLabel.setText(u"找到 %d 个符合条件的结果，双击可以使用浏览器下载种子" % len(res))

    @staticmethod
    def createButton(text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    @staticmethod
    def createComboBox(items, member=None):

        ComboBox = QtGui.QComboBox()
        ComboBox.setEditable(True)
        ComboBox.addItems(items)
        if member:
            ComboBox.activated.connect(member)
        return ComboBox

    def createTable(self):
        table = QtGui.QTableWidget(0, 2)
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        table.setHorizontalHeaderLabels((u"时间", u"标题"))
        table.horizontalHeader().resizeSection(0, 107)
        table.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        table.verticalHeader().hide()
        table.setShowGrid(False)

        table.cellActivated.connect(self.openAnimeOfItem)
        return table

    def openAnimeOfItem(self, row, column):
        item = self.res[row][2]
        # print item.text().toUtf8()
        webbrowser.open_new_tab(item)

    def questionMessage(self):
        reply = QtGui.QMessageBox.question(self, "QMessageBox.question()",
                                           u'''正在更新列表，您确定要停止上一个关键词的搜索并开始新的搜索吗？''',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        if reply == QtGui.QMessageBox.Yes:
            return True
        elif reply == QtGui.QMessageBox.Cancel:
            return False

    def writeList(self):
        write('List.dat', self.list)
        F = open('List.txt', 'w')
        F.write(u'\r\n'.join(self.listText).encode('utf-8'))
        F.close()


class Worker(QtCore.QThread):
    def __init__(self):
        super(Worker, self).__init__()
        self.keywords = ''
        self.res = []

    def setKeywords(self, keywords):
        self.keywords = keywords

    def run(self):
        s_utf = self.keywords.encode("utf-8")
        url_str = 'http://bt.ktxp.com/search.php?keyword=%s' % urllib.quote(s_utf)
        while (1):
            try:
                d = pq(url_str)
                break
            except Exception, e:
                print e
        for j in d('tbody tr'):
            div = pq(j)
            diva = div('.ttitle')
            for i in div("[title]"):
                time = pq(i).attr('title')
            for i in diva("[href^='/html']"):
                title = re.sub(r'amp;', '', re.sub(r'<[^>]*>', '', pq(i).html()))
            for i in diva("[href$='.torrent']"):
                btAdd = r'http://bt.ktxp.com' + pq(i).attr('href')
                self.res.append({'time': time,
                'title':title.encode('utf-8'),
                'address': btAdd,
                'keywords':self.keywords})
                self.emit(QtCore.SIGNAL('resultReady'), self.res)
                self.res = []

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
