#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import urllib.request as req
import os
import stat
import chardet
import zipfile
import pathlib


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

class KoreanNewsEpub:

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
                 ret += ("<p>"+s.text +"</p>")
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

    def remove_dir_tree(self, remove_dir):
        try:
            shutil.rmtree(remove_dir, ignore_errors=True)
        except(PermissionError) as e:  ## if failed, report it back to the user ##
            print("[Delete Error] %s - %s." % (e.filename, e.strerror))


    def News_Maker(self, news, many):

        what_news = Korean_news[news]['name']
        BASE_URL = Korean_news[news]['rss']
        detail_tag = Korean_news[news]['detail_tag']
        detail_ext = Korean_news[news]['detail_ext']

        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.content, "html.parser")
        recent_time = datetime.now()

        when_news = recent_time.strftime('%Y-%m-%d_%H-%M')
        news_name = what_news+when_news
        dir_name = './newspaper/epub'

        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        news_list = []

        num = 0
        for item in soup.find_all('item'):
            news_list.append(self.news_filter(item, detail_tag, detail_ext))
            num += 1
            if num == many:
                 break

        self.remove_dir_tree(dir_name)
 #       zip = zipfile.ZipFile('epub_ingredient.zip')
 #       zip.extractall('epub_ingredient')
 #       zip.close()
        shutil.copytree('epub', dir_name)

        #content.opf
        f_content = '''<?xml version='1.0' encoding='utf-8'?>
                <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
                <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <dc:language>ko</dc:language>
                <meta name="calibre:timestamp" content="'''
        f_content += when_news
        f_content += '''"/><dc:title>'''
        f_content += what_news +'</dc:title><dc:creator>'
        f_content += when_news
        f_content += '''</dc:creator>
                <meta name="cover" content="cover"/>
                <dc:identifier id="uuid_id" opf:scheme="uuid">b66f0af5-0fb2-4627-b972-a0aa9192adac</dc:identifier>
                </metadata>
                <manifest>
                <item href="cover_image.jpg" id="cover" media-type="image/jpeg"/>
                <item href="index.html" id="html" media-type="application/xhtml+xml"/>
                <item href="page_styles.css" id="page_css" media-type="text/css"/>
                <item href="stylesheet.css" id="css" media-type="text/css"/>
                <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>
                <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
                '''
        #download image
        num = 0
        for n in news_list:
            if n['image'] != None and n['image'] != '':
                tag = n['image'][-4:]
                img_name = dir_name + '/OEBPS/images/' + str(num) + tag
             #   print(img_name)
                req.urlretrieve(n['image'], img_name)
                #insert in content.opf
                f_content += '<item href="images/' + str(num) + tag+'" id="image'+str(num)+'" media-type="image/jpeg"/>'
                num += 1

        f_content +='''</manifest>
                <spine toc="ncx">
                <itemref idref="titlepage"/>
                <itemref idref="html"/>
                </spine>
                <guide>
                <reference href="titlepage.xhtml" title="Title Page" type="cover"/>
                </guide>
                </package>'''

        f = open(dir_name+'/OEBPS/content.opf', 'w+', encoding='utf-8')
        f.write(f_content)
        f.close()

        #toc.ncx
        f_toc = '''<?xml version='1.0' encoding='utf-8'?>
                <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="ko">
                  <head>
                    <meta content="b66f0af5-0fb2-4627-b972-a0aa9192adac" name="dtb:uid"/>
                    <meta content="2" name="dtb:depth"/>
                    <meta content="calibre (3.14.0)" name="dtb:generator"/>
                    <meta content="0" name="dtb:totalPageCount"/>
                    <meta content="0" name="dtb:maxPageNumber"/>
                  </head>
                  <docTitle>
                    <text>'''
        f_toc += news_name

        f_toc += '''</text>
              </docTitle>
              <navMap>
                <navPoint id="ulKRFX6xqqIlmHnj56j5YpC" playOrder="1">
                  <navLabel>
                    <text>Start</text>
                  </navLabel>
                  <content src="titlepage.xhtml"/>
                </navPoint>
              </navMap>
            </ncx>
            '''
        f = open(dir_name+'/OEBPS/toc.ncx', 'w+', encoding='utf-8')
        f.write(f_toc)
        f.close()

        # write body
        f_body = '''<?xml version='1.0' encoding='utf-8'?>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <title>'''
        f_body += news_name
        f_body += '''</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
          <link href="stylesheet.css" rel="stylesheet" type="text/css"/>
        <link href="page_styles.css" rel="stylesheet" type="text/css"/>
        </head>
        <body>'''
        f_body += '<h1>'+ what_news + '</h1>'
        f_body += '<h3>발행일자 : ' + when_news + '</h3>'

        num = 0
        for n in news_list:
            f_body += '<h4>[' + str(num+1) + '번째 뉴스]</h4>'
            f_body += '<h2>'
            for s in n['title']:
                try:
                    f_body += s
                except:
                    pass
            f_body += '</h2>'
            if n['image'] != None and n['image'] != "":
                tag = n['image'][-4:]
                f_body += '<p><img src="images/'+str(num)+tag +'" /></p>'

            for s in n['detail']:
                try:
                    f_body += s
                except:
                    pass
            num += 1
            if num == many:
                break

        f_body += '</body></html>'

        f = open(dir_name +"/OEBPS/index.html", 'w+', encoding='utf-8')
        f.write(f_body)
        f.close()

        #save
        path = pathlib.Path(dir_name).resolve()
        with zipfile.ZipFile(str(dir_name + '.epub'), 'w') as archive:
            archive.write(str(dir_name +'/mimetype'), 'mimetype',
                          compress_type=zipfile.ZIP_STORED)
            for file in path.rglob('*.*'):
             #   print(file)
                archive.write(
                    str(file), str(file.relative_to(path)),
                    compress_type=zipfile.ZIP_DEFLATED)

        shutil.copy('./newspaper/epub.epub', './newspaper/'+news_name+'.epub')
        os.remove('./newspaper/epub.epub')
        self.remove_dir_tree('epub_ingredient')
        self.remove_dir_tree(dir_name)

#News = KoreanNewsEpub(0, 20)
#News = KoreanNewsEpub(1, 10)
#News = KoreanNewsEpub(2, 10)