import sqlite3
import os


def dbwrite(res):
    hasNew = 0
    dirNow = os.getcwd()
    cx = sqlite3.connect(os.path.join(dirNow, "ktxp.db"))
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
    cu.execute(
        'CREATE TABLE IF NOT EXISTS anime_table(id INTEGER PRIMARY KEY,time string,title string UNIQUE,address string,keywords string,download interger)')
    for l in res:
        try:
            cu.execute("insert into anime_table(time,title,address,keywords,download) values('%s','%s','%s','%s',0)" % (
                l['time'], l['title'], l['add'], l['keywords']))
            hasNew += 1
        except:
            pass
    cx.commit()
    cu.close()
    cx.close()
    return hasNew


if __name__ == '__main__':
    print dbwrite('testtime', 'testtitle', 'testadd')
