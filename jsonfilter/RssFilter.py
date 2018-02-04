import json
def RssFilter(file):
    f = open(file, 'r', encoding='utf-8')
    newsarr = f.readlines()
    f.close()
    head = False
    News = []
    news = {}
    subs = []
    for na in newsarr:
        if len(na) < 3:
            head = True
            if len(subs) > 0:
                news['subs'] = subs
                News.append(news)
                news = {}
                subs = []
        else:
            if head == True:
                news['title'] = na.split('\n')[0]
                head = False
            else:
                sub_news = {}
                nsp = na.split(' http://')
                if nsp[0][len(nsp[0])-1]==" ":
                    sub_news['name'] = nsp[0][:len(nsp[0])-1]
                else:
                    sub_news['name'] = nsp[0]
                sub_news['rss'] = 'http://'+nsp[1].split('\n')[0]

                subs.append(sub_news)

    print(json.dumps(News, sort_keys=True, indent=4, separators=(',', ': ')))



#RssFilter("./newsrss.txt")
RssFilter("./ncastrss.txt")