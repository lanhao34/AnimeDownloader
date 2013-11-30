#!/usr/bin/env python
# -*- coding: utf-8 -*-


#############################################################################
##
## Copyright (C) 2010 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This animes is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this anime under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt4 import QtCore, QtGui


class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.res=[]
        self.worker=Worker()
        self.connect(self.worker, QtCore.SIGNAL('resultReady'),self.showAnimes)
        self.list=[]
        self.listText=[]

        deleteListButton = self.createButton(u"&删除", self.deleteList)
        addListButton = self.createButton(u"&添加", self.addList)
        downloadButton = self.createButton(u"&下载", self.download)
        searchButton = self.createButton(u"&搜索", self.search)
        readButton = self.createButton(u"&读取数据库", self.read)
        dbwriteButton = self.createButton(u"&写入数据库", self.dbwrite)
        dbdeleteButton = self.createButton(u"&删除条目", self.dbdelete)

        self.animeTitle,self.searchName,self.subTeams=read()
        self.listComboBox=self.createComboBox(self.listText,self.updateComboBoxs)
        self.listComboBox.setEditable(False)
        self.titleComboBox=self.createComboBox(self.animeTitle,self.updateSubTeamComboBox)
        self.subTeamComboBox=self.createComboBox([u'请先选择动漫'])
        self.subComboBox=self.createComboBox([u'',u'GB',u'BIG',u'简', u'繁', u'繁體',u'簡繁'])
        self.HDComboBox=self.createComboBox([u'',u'720P',u'480P',u'1080P'])
        self.userComboBox=QtGui.QLineEdit()

        self.createanimesTable()

        # self.directoryComboBox = self.createComboBox(QtCore.QDir.currentPath())
        subLabel = QtGui.QLabel(u" 字体:")
        HDLabel = QtGui.QLabel(u" 清晰度:")
        userLabel = QtGui.QLabel(u"其他关键字:")
        self.animesFoundLabel = QtGui.QLabel()

        buttonsLayout = QtGui.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(readButton)
        buttonsLayout.addWidget(dbwriteButton)
        buttonsLayout.addWidget(dbdeleteButton)
        # buttonsLayout.addWidget(downloadButton)

        mainLayout = QtGui.QGridLayout()
        # mainLayout.addWidget(animeLabel, 0, 0)
        # mainLayout.addWidget(self.animeComboBox, 0, 1, 1, 2)
        # mainLayout.addWidget(textLabel, 1, 0)
        # mainLayout.addWidget(self.textComboBox, 1, 1, 1, 2)
        # mainLayout.addWidget(directoryLabel, 2, 0)
        mainLayout.addWidget(self.listComboBox, 0, 0, 1, 6)
        mainLayout.addWidget(addListButton, 0, 6, 1, 1)
        mainLayout.addWidget(deleteListButton, 0, 7, 1, 1)
        mainLayout.addWidget(self.titleComboBox, 1, 0, 1, 4)
        mainLayout.addWidget(self.subTeamComboBox, 1, 4, 1, 2)
        mainLayout.addWidget(searchButton, 1, 6, 1, 1)
        mainLayout.addWidget(subLabel, 2, 0, 1, 1)
        mainLayout.addWidget(self.subComboBox, 2, 1, 1, 1)
        mainLayout.addWidget(HDLabel, 2, 2, 1, 1)
        mainLayout.addWidget(self.HDComboBox, 2, 3, 1, 1)
        mainLayout.addWidget(userLabel, 2, 4, 1, 1)
        mainLayout.addWidget(self.userComboBox, 2, 5, 1, 3)
        mainLayout.addWidget(self.animesTable, 4, 0, 1, 8)
        mainLayout.addWidget(self.animesFoundLabel, 5, 0, 1, 0)
        # mainLayout.addWidget(readButton, 4, 2, 1, 1)
        mainLayout.addLayout(buttonsLayout, 6, 5, 1, 3)
        self.setLayout(mainLayout)

        self.setWindowTitle(u"极影动漫下载")
        self.setWindowIcon(QtGui.QIcon('dango.ico'))
        self.resize(600, 300)

    def download(self):
        for Range in self.animesTable.selectedRanges():
            for i in self.res[Range.topRow():Range.bottomRow()+1]:
                print i[2]
    def dbwrite(self):
        dbwrite(self.res)
    def dbdelete(self):
        cx = sqlite3.connect("ktxp.db")
        cx.isolation_level = None
        cx.text_factory = str
        cu = cx.cursor()
        index=[]
        for Range in self.animesTable.selectedRanges():
            for i in range(Range.topRow(),Range.bottomRow()+1):
                index.append(i)
                cu.execute("delete from t1 where title=?",(self.res[i][1],))
        cx.commit()
        cu.close()
        cx.close()
        index.sort(reverse=True)
        for i in index:
            print i
            self.animesTable.removeRow(i)
    # @staticmethod
    def updateSubTeamComboBox(self):
        self.subTeamComboBox.clear()
        try:
            index=self.titleComboBox.currentIndex()
        except Exception, e:
            index=0
        self.subTeamComboBox.addItems(self.subTeams[index].keys())
    def updateComboBoxs(self):
        title,subTeam,sub,HD,user=self.list[self.listComboBox.currentIndex()]
        self.titleComboBox.setEditText(title)
        self.updateSubTeamComboBox()
        self.subTeamComboBox.setEditText(subTeam)
        self.subComboBox.setEditText(sub)
        self.HDComboBox.setEditText(HD)
        self.userComboBox.setText(user)
    def addList(self):
        self.list.append([unicode(self.titleComboBox.currentText()),unicode(self.subTeamComboBox.currentText()),unicode(self.subComboBox.currentText()),unicode(self.HDComboBox.currentText()),unicode(self.userComboBox.text())])
        self.listText.append(u' '.join(self.list[-1]))
        self.listComboBox.insertItem(0,self.listText[-1])
        self.listComboBox.setCurrentIndex(0)
    def deleteList(self):
        index=self.listComboBox.currentIndex()
        del(self.list[index])
        del(self.listText[index])
        self.listComboBox.removeItem(index)
    def search(self):
        if self.worker.isRunning():
            if self.questionMessage():
                self.worker.exit()
            else:
                return
        try:
            title=self.searchName[self.titleComboBox.currentIndex()]
        except Exception, e:
            title=unicode(self.titleComboBox.currentText())
            print e
        keywords=u'+'.join([title,unicode(self.subTeamComboBox.currentText()),unicode(self.subComboBox.currentText()),unicode(self.HDComboBox.currentText()),unicode(self.userComboBox.text())])
        self.worker.setKeywords(keywords)
        self.worker.start()
        self.animesFoundLabel.setText(u"正在更新列表...")
    def read(self):
        self.animesTable.setRowCount(0)

        cx = sqlite3.connect("ktxp.db")
        cx.isolation_level = None
        cx.text_factory = str
        cu = cx.cursor()
        cu.execute("select subTime,title,btAdd from t1 Order by subTime desc")
        res = cu.fetchall()
        cu.close()
        cx.close()

        self.showAnimes(res)

    def showAnimes(self,res):
        self.res=res
        self.animesTable.setRowCount(0)
        self.animesTable.clearContents()
        for (time,name,add) in res:
            timeItem = QtGui.QTableWidgetItem(time)
            timeItem.setFlags(timeItem.flags() ^ QtCore.Qt.ItemIsEditable)
            titleItem = QtGui.QTableWidgetItem(name.decode('utf-8'))
            titleItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.animesTable.rowCount()
            self.animesTable.insertRow(row)
            self.animesTable.setItem(row, 0, timeItem)
            self.animesTable.setItem(row, 1, titleItem)

        self.animesFoundLabel.setText(u"找到 %d 个符合条件的结果，双击可以使用浏览器下载种子" % len(res))

    def createButton(self, text, member):
        button = QtGui.QPushButton(text)
        button.clicked.connect(member)
        return button

    def createComboBox(self, items, member=None):

        ComboBox = QtGui.QComboBox()
        ComboBox.setEditable(True)
        ComboBox.addItems(items)
        if member:
            ComboBox.activated.connect(member)
        return ComboBox

    def createanimesTable(self):
        self.animesTable = QtGui.QTableWidget(0, 2)
        self.animesTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        self.animesTable.setHorizontalHeaderLabels(("Time", "Title"))
        self.animesTable.horizontalHeader().resizeSection(0,107)
        self.animesTable.horizontalHeader().setResizeMode(1,QtGui.QHeaderView.Stretch)
        self.animesTable.verticalHeader().hide()
        self.animesTable.setShowGrid(False)

        self.animesTable.cellActivated.connect(self.openAnimeOfItem)

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
class Worker(QtCore.QThread):
    def __init__(self):
        super(Worker, self).__init__()
        self.keywords=[]
        self.res = []
    def setKeywords(self,keywords):
            self.keywords=keywords
    def run(self):
        while(1):
            try:
                # print keywords
                s_utf=self.keywords.encode("utf-8")
                url_str='http://bt.ktxp.com/search.php?keyword=%s'%urllib.quote(s_utf)
                d = pq(url_str)
                break
            except Exception , e:
                print e
        for j in d('tbody tr'):
            div=pq(j)
            diva=div('.ttitle')
            for i in div("[title]"):
                time=pq(i).attr('title')
            for i in diva("[href^='/html']"):
                title=re.sub(r'amp;','',re.sub(r'<[^>]*>','', pq(i).html()))
            for i in diva("[href$='.torrent']"):
                btAdd=r'http://bt.ktxp.com'+pq(i).attr('href')
                self.res.append([time,title.encode('utf-8'),btAdd])
        self.emit(QtCore.SIGNAL('resultReady'),self.res)
        self.res = []
def read():
    import pickle
    F=open('Anime.dat','r')
    animes=pickle.load(F)
    F.close()
    return animes
if __name__ == '__main__':

    import re
    import sys
    import urllib
    import sqlite3
    import webbrowser
    from dbwrite import dbwrite
    from pyquery import PyQuery as pq

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
