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


class ContentToEpub:
    def __init__(self, LANGUAGE, RANGE, URL, LINEOFF):
        self.MakeBook(LANGUAGE, RANGE, URL, LINEOFF)

    def urls_append(self, soup_resource, selecting, tag, attr):
        subarticles = []
        try:
            for s in soup_resource.select(selecting):
                print(s)
                for t in s.get_all(tag):
                    print(t)
                    subarticles["url"] = t.get(attr)
                    print(t.get(attr))
        except: pass
        return subarticles

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

    def title_filter(self, string):
        string = string.replace("_", " ", 100)
        special_string = ["/", ":", ";", "*", "~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "=", "?", "[", "]", "<",
                          ">", "(", ")", "\n", "\t", "\r", "|"]
        for ss in special_string:
            string = string.replace(ss, "", 10)
        print(string)
        return string

    def get_contents_title_text_image_order(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = self.title_filter(soup.title.string)
        hs = soup.select('h1')
        hs.append(soup.select('h2'))
        hs.append(soup.select('h3'))
        hs.append(soup.select('h4'))
        texts = soup.select('p')
        images_ = soup.select('img')
        images = []
        for i in images_:
            images.append(i['src'])
        orders = []
        for tag in soup.find_all(True):
            if tag.name == "p" or tag.name == "img" or tag.name == "h1" or tag.name == "h2" or tag.name == "h3" or tag.name == "h4":
                orders.append(tag.name)
 #       print("{0}+{1} = {2} ? {3}".format(len(bodys), len(images), len(orders), len(bodys)+len(images)==len(orders)))
        return title, texts, images, orders[:-17]


    def image_attach(self, image_url, storage_name):
        try:
            req.urlretrieve(image_url,  storage_name)
            return True
        except: return False

    def get_body(self, contents, dir_name):
        image_tag = False
        body = ""
        ran = random.randrange(1000000)
        p, i = 0, 0
        for e in contents['order']:
            if e == 'p':
                if(image_tag):
                    body += "<p>" + contents['text'][p].text + "</p>\n"
                    image_tag = False
                else:
                #    print(contents['text'][p].text)
                    if contents['text'][p].text.find(">")>0 or contents['text'][p].text.find("<")>0:
                          pass
                    else: body += "<p>"+ contents['text'][p].text+"</p>\n"

                p += 1
            elif e == 'i':
                http_name = contents['image'][i]
                if http_name.find(".jpg") > 1:
                     new_name = str(ran)+str(i) + ".jpg"
                elif http_name.find(".png") > 1:
                     new_name = str(ran)+str(i) + ".png"
                else:
                    new_name = str(ran)+str(i) + ".gif"
                    if self.image_attach(http_name, dir_name+'/images/'+new_name):
                        body += "<p class='image'><img src='images/"+new_name+"'/></p>\n"
                        image_tag = True
                i += 1
            else:
                body += "<"+e+">" + contents['text'][p].text + "</"+e+">\n"
        return body

    def remove_dir_tree(self, remove_dir):
        try:
            shutil.rmtree(remove_dir, ignore_errors=True)
        except(PermissionError) as e:  ## if failed, report it back to the user ##
            print("[Delete Error] %s - %s." % (e.filename, e.strerror))

    def make_file(self, file_name, string):
        f = open(file_name, 'w+', encoding='utf-8')
        f.write(string)
        f.close()

    def get_contents_title_text(self, url, lineoff):
        title = self.title_filter(os.path.basename(url))[:-4]
        body = ""
        file = open(url, 'r', encoding='utf-8')
        if lineoff:
            tmp_body = ""
            for line in file.readlines():
                tmp_body += line
            split_body = tmp_body.split(".\n", 10000)
            for bod in split_body:
                bo = bod.split("\n\n", 1000)
                for i in range(len(bo)):
                    if i == len(bo)-1:
                        body += "<p>"+bo[i]+".</p>"
                    else:
                        body += "<p>"+bo[i]+"</p>"
        else:
            for line in file.readlines():
                body += "<p>"+line+"</p>"

        file.close()
        return title, body

    def MakeBook(self, LANGUAGE, RANGE, URL, LINEOFF):
        url = URL
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        parent_dir_name = './content'
        dir_name = parent_dir_name + '/OEBPS'
        uuid = "b66f0af5-0fb2-4627-b972-dx"+"{0:10}".format(random.randrange(1, 1000000000))
#        zip = zipfile.ZipFile('epub.zip')
#        zip.extractall(parent_dir_name)
#        zip.close()

        if os.path.isdir(parent_dir_name):
            self.remove_dir_tree(parent_dir_name)
        shutil.copytree('epub-sample', parent_dir_name)

#        os.mkdir(parent_dir_name)
#        os.mkdir(dir_name)
#        os.mkdir(parent_dir_name+'META-INF')


        contents = {}
        contents['url'] = URL
        body = ""
#        print(contents)
        if RANGE == "html":
            contents['title'], contents['text'], contents['image'], contents['order'] = self.get_contents_title_text_image_order(contents['url'])
            body = self.get_body(contents, dir_name)
        elif RANGE == "text":
            contents['title'], body = self.get_contents_title_text(contents['url'], LINEOFF)

        titlepagexhtml = '''<?xml version='1.0' encoding='utf-8'?>
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="'''+LANGUAGE+'''">
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
                <meta name="cover" content="true"/>
                <title>드리는 말씀</title>
                <style type="text/css" title="override_css">
                    @page {padding: 0pt; margin:0pt}
                    body { text-align: center; padding:0pt; margin: 0pt; }
                </style>
            </head>
            <body>
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="100%" height="100%" viewBox="0 0 1200 1600" preserveAspectRatio="none">
                        <image width="1200" height="1600" xlink:href="ebook_image.jpg"/>
                    </svg>
                </div>
            <p>※주의 : 이 책의 저작권은 [''' + contents['title'] + ''']의 해당 저자들에게 있습니다. 무단복제 및 무단배포할 경우 저작권법에 저촉될 수 있습니다.</p>
                <p>반드시 개인적으로 보아주시기 바랍니다.</p>
            </body>
        </html>
                '''
        self.make_file(dir_name + '/titlepage.xhtml', titlepagexhtml)
        del titlepagexhtml

        tocncx = '''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="'''+LANGUAGE+'''">
  <head>
    <meta content="'''+uuid+'''" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="soori (3.14.0)" name="dtb:generator"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>'''+contents['title']+'''</text>
  </docTitle>
  <navMap>
      <navPoint id="np1" playOrder="1">
      <navLabel>
        <text>드리는 말씀</text>
      </navLabel>
      <content src="titlepage.xhtml"/>
    </navPoint>
    '''
        tocncx += '<navPoint id="np'+str(2)+'" playOrder="'+str(2)+'">\n'
        tocncx += '<navLabel><text>'+contents['title']+'</text></navLabel>\n'
        tocncx += '<content src="html.html#item'+str(0)+'"/></navPoint>'
        tocncx += '''</navMap>
</ncx>'''

        self.make_file(dir_name + "/toc.ncx", tocncx)
        del tocncx

        html = "<?xml version='1.0' encoding='utf-8'?>\n<html xmlns='http://www.w3.org/1999/xhtml'>\n"
        html += "<head><title>"+contents['title']+"</title></head>\n"
        html += "<body>\n<h1>"+contents['title']+"</h1><p>DATE : "+ date +"</p>"+body+"</body>\n</html>"

        self.make_file(dir_name + "/index.html", html)
        del html


        contentopf = '''<?xml version='1.0' encoding='utf-8'?>
        <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
        <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/" 
        xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <dc:language>'''+LANGUAGE+'''</dc:language>
            <meta name="calibre:timestamp" content="''' + str(date) + "T" + str(time) \
                     + '''"/>
            <dc:title> ''' + contents['title'] + '''</dc:title>
            <dc:creator>'''+ str(date) + '''</dc:creator>
            <meta name="cover" content="cover"/>
            <dc:identifier id="uuid_id" opf:scheme="uuid">''' + uuid + '''</dc:identifier>
          </metadata>
          <manifest>
            <item href="news_image.jpg" id="news_image" media-type="image/jpeg"/>
            <item href="ncast_image.jpg" id="ncast_image" media-type="image/jpeg"/>
            <item href="ebook_image.jpg" id="ebook_image" media-type="image/jpeg"/>
            <item href="index.html" id="html" media-type="application/xhtml+xml"/>
            <item href="page_styles.css" id="page_css" media-type="text/css"/>
            <item href="stylesheet.css" id="css" media-type="text/css"/>
            <item href="titlepage.xhtml" id="titlepage" media-type="application/xhtml+xml"/>
            <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>\n'''


        n = 0
        for root, dirs, ims in os.walk(dir_name + '/images'):
            for i in ims:
                itype = "jpeg"
                if i.find('png')>1: itype = "png"
                elif i.find('gif')>1: itype = "gif"

                contentopf += '<item href="images/' + i + '" id="image' + str(n + 1) + '" media-type="image/'+itype+'"/>\n'
                n += 1

        contentopf += '''
          </manifest>
          <spine toc="ncx">
            <itemref idref="titlepage"/>
            <itemref idref="html"/>
          </spine>
          <guide>
            <reference href="titlepage.xhtml" title="Title Page" type="cover"/>
          </guide>
        </package>
                '''
        self.make_file(dir_name + "/content.opf", contentopf)
        del contentopf

        #save

        path = pathlib.Path(parent_dir_name).resolve()
        with zipfile.ZipFile(str(contents['title'] + '.epub'), 'w') as archive:
            archive.write(str(parent_dir_name +'/mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
            for file in path.rglob('*.*'):
            #    print(file)
                archive.write(str(file), str(file.relative_to(path)), compress_type=zipfile.ZIP_DEFLATED)

        self.remove_dir_tree(parent_dir_name)
