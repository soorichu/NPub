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

    #Override
    def get_contents_title_text_image_order(self, url, body_tag):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = self.title_filter(soup.title.string)
        body = soup.select(body_tag)
        texts = []
        for b in body:
            bd = b.text
            for s in bd.split("\n", 1000):
                if s == "" or s=="\n": pass
                else:
                    try:
                        texts.append("<p>"+s+"</p>")
                    except: pass

        images_ = soup.select('img')
        images = []
        for i in images_:
            try:
                if len(i['alt'])>0:
                    images.append(i['src'])
            except: pass
        orders = ""
        for tag in soup.find_all(True):
            if tag.name == "img":
                orders += "i"
            else:
                orders += "p"
                #       print("{0}+{1} = {2} ? {3}".format(len(bodys), len(images), len(orders), len(bodys)+len(images)==len(orders)))
        return title, texts, images, orders

    #Override
    def get_body(self, contents, dir_name):
        body = ""
        for n in range(len(contents)):
            body += "<hr/>"
            body += "<h2 id='item"+str(n)+"' >"+contents[n]['title']+"</h2>\n"
            ran = random.randrange(1000000)
            num = 0
            '''
            for image in contents[n]['image']:
                if image[:4] == "http" and image[-4:-3]==".":
                    image_tag = image[-4:]
                    new_name = str(ran)+str(num)+image_tag
                 #   print(new_name)
                    if self.image_attach(image, dir_name+"/images/"+new_name):
                        body += "<p class='image'><img src='images/"+new_name+"'/></p>\n"
                    num += 1
            '''
            for text in contents[n]['text']:
                txt = self.html_special_filter(text[3:-4])
                body += "<p>"+txt+"</p>"
        return body

    def get_text_body(self, contents):
        body = ""
        for content in contents:
            body += "####" + content['title']+"####\n"
            for text in content['text']:
                body += text[3:-4]+"\n"
            body += "\n"
        return body


    def MakeBook(self, RANGE, CONTENT, FORMAT):
        title = CONTENT['title']+"-"+ CONTENT['subs']['name']
        rss = CONTENT['subs']['rss']
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        parent_dir_name = './content'
        dir_name = parent_dir_name + '/OEBPS'
        uuid = "b66f0af5-0fb2-4627-b972-dx"+"{0:10}".format(random.randrange(1, 1000000000))
        if CONTENT['title'] == "코리아타임즈" or CONTENT['subs']['name'] == "[코리아헤럴드]":
            LANGUAGE = "en"
        else:
            LANGUAGE = "ko"

        contents = self.get_contents_urls(rss)

        for i in range(len(contents)):
            contents[i]['title'], contents[i]['text'], contents[i]['image'], contents[i]['order'] = \
                self.get_contents_title_text_image_order(contents[i]['url'], CONTENT['body_tag'])

        if FORMAT == "epub":
            self.make_content_folder(parent_dir_name)
            self.make_file(dir_name+'/titlepage.xhtml', self.titlepagehtml(title, RANGE))
            self.make_file(dir_name + "/toc.ncx", self.tocncx(uuid, title, contents, LANGUAGE))

            html = "<?xml version='1.0' encoding='utf-8'?>\n<html xmlns='http://www.w3.org/1999/xhtml' xml:lang='"+LANGUAGE+"'>\n"
            html += "<head><title>"+title+"</title></head>\n"
            html += "<body>\n<h1>"+title+"</h1><p>DATE : "+ date +"</p>"+self.get_body(contents, dir_name) +"</body>\n</html>"

            self.make_file(dir_name + "/index.html", html)
            del html
            del contents

            self.make_file(dir_name + "/content.opf", self.contentopf(uuid, date, time, title, dir_name))

            #save
            self.make_epub(parent_dir_name, title)
        else:
            f = open(title+".txt", "w", encoding="utf-8")
            f.write("NEWS : " +title +"\n"+"DATE : "+date +" "+ time+"\n\n")
            f.write(self.get_text_body(contents))
            f.close()
