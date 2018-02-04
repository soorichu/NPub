#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

Korean_news = [
    {
        "name": "조선일보",
        "rss": "http://myhome.chosun.com/rss/www_section_rss.xml",
        "detail_tag": "div.par",
        "detail_ext": ".html"

    },

    {
        "name": "중앙일보",
        "rss": "http://rss.joins.com/joins_homenews_list.xml",
        "detail_tag": "div#article_body",
        "detail_ext": "_list"

    },

    {
        "name": "한겨레",
        "rss": "http://www.hani.co.kr/rss/lead/",
        "detail_tag": "div.text",
        "detail_ext": ".html"

    },

]

class KoreanNewsTxt:

    def __init__(self, which_news, how_many):
        self.which_news = which_news
        self.how_many = how_many
        self.News_Maker(self.which_news, self.how_many)

    def find_http(self, http, detail_ext):
        str = http.text
        return (str[str.find("http", 0, len(str)):str.find(detail_ext, 0, len(str))+len(detail_ext)])

    def find_image(self, http_string):
        ret = ""
        try:
            response = requests.get(http_string)
            soup = BeautifulSoup(response.content, "html.parser")
            ret = soup.img['src']
        except:
            ret = ""
        return ret

    def find_detail(self, http_string, detail_tag):
        ret = ""
        try:
            response = requests.get(http_string)
            soup = BeautifulSoup(response.content, "html.parser")
        except:
            return ret
        for s in soup.select(detail_tag):
            try:
                 ret += (s.text +"\n")
            except:
                ret += ""
        return ret

    def news_filter(self, item, detail_tag, detail_ext):
        newsdic = {}
        http = self.find_http(item, detail_ext)
        newsdic['title'] = item.title.string
        newsdic['http'] = http
        newsdic['image'] = self.find_image(http)
        newsdic['detail']= self.find_detail(http, detail_tag)
        return newsdic


    def News_Maker(self, news, many):

        what_news = Korean_news[news]['name']
        BASE_URL = Korean_news[news]['rss']
        detail_tag = Korean_news[news]['detail_tag']
        detail_ext = Korean_news[news]['detail_ext']

        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        recent_time = datetime.now()

        when_news = recent_time.strftime('%Y-%m-%d_%H-%M')
        news_name = what_news+when_news+".txt"
        news_list = []
        dir_name = './newspaper'

        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        num = 0
        for item in soup.find_all('item'):
            news_list.append(self.news_filter(item, detail_tag, detail_ext))
            num += 1
            if num == many:
                 break

        num = 0

        f = open(dir_name +'/'+news_name, 'w', encoding='utf-8')
        f.write(what_news)
        f.write("\n발행일자 : "+when_news+"\n\n")
        for n in news_list:
            f.write("[{0}번째 뉴스]\n".format(num+1))
            f.write("제목: ")
            for s in n['title']:
                try:
                    f.write(s)
                except:
                    pass
                 #   f.write(s.decode('cp949'))
            f.write('\n')
        #    f.write("연결: {0}\n".format(n['http']))
        #    f.write("사진: {0}\n".format(n['image']))
            for s in n['detail']:
                try:
                    f.write(s)
                except:
                    pass
                 #   f.write(s.decode('cp949'))
            f.write('\n')
            num += 1
            if num == many:
                f.close()
                break

#조선일보 기사 20개 : News = KoreanNewsTxt(0, 20)    #조선일보가 가장 잘 됩니다.
#중앙일보 기사 10개 : News = KoreanNewsTxt(1, 10)
#한겨레 기사 15개 : News = KoreanNewsTxt(2, 15)

#News = KoreanNewsTxt(0, 20)