# -*- coding: utf-8 -*-
import jft
def write(web):
    import pickle
    import re
    import urllib
    from pyquery import PyQuery as pq
    animeTitle=[]
    searchName=[]
    subTeams=[]
    datas=re.findall("(?<=array\.push\(\[)(.*)?(?=\]\)\;)",web)
    allSubTeams={}
    for data in datas:
        data=data.split(',')
        teams={}
        # print data[1][1:-1],urllib.unquote(data[2][1:-1])
        d=pq('<html>'+data[3][1:-1]+'</html>')
        for i in d('a'):
            da=pq(i)
            teams.update({f2j(da.text().encode('utf-8')):da.attr('href')})
            allSubTeams.update(teams)
        animeTitle.append(f2j(data[1][1:-1]))
        searchName.append(urllib.unquote(data[2][1:-1]).decode('utf-8'))
        subTeams.append(teams)
    animeTitle.insert(0,'')
    searchName.insert(0,'')
    subTeams.insert(0,allSubTeams)
    anime=[animeTitle,searchName,subTeams]
    F=open('Anime.dat','w')
    pickle.dump(anime,F)
    F.close()
def f2j(title):
    title=title.decode('utf-8')
    strTemp=''
    for j in range(len(title)):
        charTemp=title[j].encode('utf-8')
        if u'\u4E00'<title[j]<u'\u9FFF':
            charTemp=jft.f2j('utf-8','utf-8',charTemp)
        strTemp+=charTemp
    return strTemp.decode('utf-8')
def get_web():
    import urllib
    url="http://share.dmhy.org/cms/page/name/programme.html"
    web=urllib.urlopen(url).read()
    # print web
    return web
def read():
    import pickle
    F=open('Anime.dat','r')
    anime=pickle.load(F)
    F.close()
    return anime
if __name__ == '__main__':
    write(get_web())
    # animeTitle,searchName,subTeams=read()
    # for i in range(len(animeTitle)):
    #     print animeTitle[i],subTeams[i].keys()

