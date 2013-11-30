import sqlite3
import os
def dbwrite(res):
    hasNew=0
    dirNow=os.getcwd()
    cx = sqlite3.connect(os.path.join(dirNow,"ktxp.db"))
    cx.isolation_level = None
    cx.text_factory = str
    cu = cx.cursor()
    cu.execute('create table if not exists t1(id integer primary key,subTime string,title string UNIQUE,btAdd string)')
    for time,title,add in res:
        try:
            cu.execute("insert into t1(subTime,title,btAdd) values('%s','%s','%s')"%(time,title,add))
            print time,title
            hasNew+=1
        except:
            pass
    cx.commit()
    cu.close()
    cx.close()
    return hasNew
if __name__ == '__main__':
    print dbwrite('testtime','testtitle','testadd')
