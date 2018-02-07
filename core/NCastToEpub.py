#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import os
import random
import requests


from core.ToEpubCore import ToEpubCore


class NCastToEpub(ToEpubCore):

    def __init__(self, RANGE, CONTENT):
        self.range = RANGE
        self.MakeBook(RANGE, CONTENT)

    def get_contents_urls(self, rss):
        contents_urls = []
        response = requests.get(rss)
        soup = BeautifulSoup(response.content, "html.parser")
        for ss in soup.select('strong.title'):
            for ssa in ss.find_all('a'):
                sssa = ssa.get('href')
                if len(sssa) > 10:
                    temp_dic = {}
                    temp_dic["url"] = "http://terms.naver.com"+sssa
                    contents_urls.append(temp_dic)
        return contents_urls

    #Override
    def get_contents_title_text_image_order(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string
        texts = soup.select('p')
        images_ = soup.select('img')
        images = []
        for i in images_:
            images.append(i['src'])
        orders = ""
        for tag in soup.find_all(True):
            if tag.name == "p":
                orders += "p"
            elif tag.name == "img":
                orders += "i"
 #       print("{0}+{1} = {2} ? {3}".format(len(bodys), len(images), len(orders), len(bodys)+len(images)==len(orders)))
        return title, texts, images, orders[:-17]


    def MakeBook(self, RANGE, CONTENT):
        RANGE = RANGE
        CONTENT = CONTENT
        LANGUAGE = "ko"
        print(CONTENT)
        title = CONTENT['title']+"-"+ CONTENT['subs']['name']
        rss = CONTENT['subs']['rss']
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        parent_dir_name = './content'
        dir_name = parent_dir_name + '/OEBPS'
        uuid = "b66f0af5-0fb2-4627-b972-dx"+"{0:10}".format(random.randrange(1, 1000000000))

        self.make_content_folder(parent_dir_name)
        self.make_file(dir_name+'/titlepage.xhtml', self.titlepagehtml(title, RANGE))

        contents = self.get_contents_urls(rss)
#        print(contents)

        for i in range(len(contents)):
            contents[i]['title'], contents[i]['text'], contents[i]['image'], contents[i]['order'] = self.get_contents_title_text_image_order(contents[i]['url'])

        self.make_file(dir_name + "/toc.ncx", self.tocncx(uuid, title, contents, LANGUAGE))

        html = "<?xml version='1.0' encoding='utf-8'?>\n<html xmlns='http://www.w3.org/1999/xhtml'>\n"
        html += "<head><title>"+title+"</title></head>\n"
        html += "<body>\n<h1>"+title+"</h1><p>DATE : "+ date +"</p>"+self.get_body(contents, dir_name) +"</body>\n</html>"

        self.make_file(dir_name + "/index.html", html)
        del html
        del contents

        self.make_file(dir_name + "/content.opf", self.contentopf(uuid, date, time, title, dir_name))

        #save
        self.make_epub(parent_dir_name, title)