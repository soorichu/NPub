#-*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import urllib.request as req
import os
import random
import zipfile
import pathlib
from core.ToEpubCore import ToEpubCore


class NewsToEpub(ToEpubCore):
    def __init__(self, RANGE, CONTENT, FORMAT, NUMBER):
        self.range = RANGE
        self.number = NUMBER
        self.MakeBook(RANGE, CONTENT, FORMAT)

    def get_contents_urls(self, rss):
        response = requests.get(rss)
        soup = BeautifulSoup(response.content, "html.parser")
        contents = []
        count = 0
        for item in soup.select('item'):
            cont = {}
            start = item.text.find('http', 0, len(item.text))
            end = item.text.find('\n', item.text.find('http', 0, len(item.text)), len(item.text))
            url = item.text[start:end]
            if url[-1:] == '\r': url = url[:-1]
            cont['url'] = url
            contents.append(cont)
            count += 1
            if count == self.number:
                break
     #   print(contents)
        return contents

    def MakeBook(self, RANGE, CONTENT, FORMAT):
        LANGUAGE = "ko"
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
    #    print(self.get_contents_title_text_image_order(contents[0]['url']))

        for i in range(len(contents)):
            contents[i]['title'], contents[i]['text'], contents[i]['image'], contents[i]['order'] = self.get_contents_title_text_image_order(contents[i]['url'])

        print(contents)
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
