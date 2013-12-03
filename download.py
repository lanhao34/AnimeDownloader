# -*- coding: utf-8 -*-
import re
import os
import time
from string import atoi
import lx.lixian_commands as lxcmd
from PyQt4 import QtCore, QtGui
from anime_commands import *


class Anime:
    def __init__(self, name, subteam):
        self.name = name
        self.subteam = subteam


class DownloadTab(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DownloadTab, self).__init__(parent)
        self.downloadTable = self.createTable()
        self.tasks = read('Tasks.dat')
        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.downloadTable, 3, 0)
        self.setLayout(mainLayout)

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
        table = QtGui.QTableWidget(0, 3)
        table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        table.setHorizontalHeaderLabels((u"时间", u"标题", u"进度"))
        table.horizontalHeader().resizeSection(0, 107)
        table.horizontalHeader().resizeSection(1, 550)
        table.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.Stretch)
        table.verticalHeader().hide()
        table.setShowGrid(False)

        table.cellActivated.connect(self.download)
        return table

    def download(self, row, column):
        item = self.res[row][2]
        print item.text().toUtf8()

    def showAnimes(self, tasks):
        self.tasks = tasks+self.tasks
        self.animeTable.setRowCount(0)
        self.animeTable.clearContents()
        for task in self.tasks:
            timeItem = QtGui.QTableWidgetItem(task['time'])
            timeItem.setFlags(timeItem.flags() ^ QtCore.Qt.ItemIsEditable)
            titleItem = QtGui.QTableWidgetItem(task['title'].decode('utf-8'))
            titleItem.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            titleItem.setFlags(titleItem.flags() ^ QtCore.Qt.ItemIsEditable)

            row = self.animeTable.rowCount()
            self.animeTable.insertRow(row)
            self.animeTable.setItem(row, 0, timeItem)
            self.animeTable.setItem(row, 1, titleItem)


class Worker(QtCore.QThread):
    def __init__(self):
        super(Worker, self).__init__()

    def run(self):
        title = re.sub(r'\\', r'﹨'.decode('utf8').encode('gbk'), re.sub(r'\"', r'',
                                                                        re.sub(r'/', r'∕'.decode('utf8').encode('gbk'),
                                                                               title.decode('utf8').encode('gbk'))))
        add = btAdd.encode('utf8')
        for i in range(0, 9):
            try:
                t = lxcmd.add.add_task(['--bt', add])[0]
                if not t['status'] == 2:
                    time.sleep(600)
                while not t['status'] == 2:
                    time.sleep(600)
                    t = lxcmd.add.add_task(['--bt', add])[0]
                    break
                break
            except Exception, e:
                print e
                time.sleep(10)
        downloadpath += '\\' + self.dirName(title, self.get_num(t))
        if t['name'].find('EMD') >= 0:
            for i in range(0, 9):
                try:
                    lxcmd.download.download_task([t['id'] + "/.mp4", "--output-dir", downloadpath, "-c"])
                    break
                except Exception, ex:
                    print Exception, ":", ex
                    time.sleep(10)
        else:
            for i in range(0, 9):
                try:
                    lxcmd.download.download_task([t['id'], "--output-dir", downloadpath, "-c"])
                    break
                except Exception, ex:
                    print Exception, ":", ex
                    time.sleep(10)
        lxcmd.delete.delete_task([t['id']])

    def get_num(self, t):
        try:
            Nums = re.findall("(?<=\[)(\d+-\d+)?(?=\])", t['name'])
            Num = Nums[0].split('-')
            if abs(atoi(Num[0]) - atoi(Num[1])) >= 5:
                print "已完结".decode('utf').encode('gbk')
                return 1
        except:
            pass
        if t['name'].find('ALL') >= 0:
            print "已完结".decode('utf').encode('gbk')
            return 1
        Nums = re.findall("(?<=\[)(\d+)(?:v\d+|_\w+)?(?=\])", t['name'])
        dellist = ['720', '576']
        for i in Nums:
            if len(i) > 3:
                dellist.append(i)
        for i in dellist:
            try:
                Nums.remove(i)
            except:
                pass
        try:
            return max(Nums)
        except Exception, e:
            print e
            Nums = []
            tmp_t = lxcmd.list.list_task([t['id'] + '/', '--name'])
            print tmp_t
            for i in tmp_t:
                filename = i['name']
                Nums += re.findall("(?<=\[)(\d+)(?:v\d+|_\d+)?(?=\])", filename)
            dellist = ['720', '576']
            for i in Nums:
                if len(i) > 3:
                    dellist.append(i)
            for i in dellist:
                try:
                    Nums.remove(i)
                except:
                    pass
            try:
                if atoi(max(Nums)) - atoi(min(Nums)) >= 5:
                    print "已完结".decode('utf').encode('gbk')
                    return 1
                return max(Nums)
            except Exception, e:
                print e
                return ''

    def dirName(self, keywords, num):
        for i in range(keywords.count('')):
            keywords.remove('')
        dir_name = '[' + ']['.join(keywords) + ']'
        return dir_name


if __name__ == '__main__':
    os.system('pause')
