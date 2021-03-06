#-*- coding: utf-8 -*-
import codecs

import requests
from bs4 import BeautifulSoup
import shutil
import urllib.request as req
import os
import random
import zipfile
import pathlib


class ToEpubCore:

    def urls_append(self, soup_resource, selecting, tag, attr):
        subarticles = []
        try:
            for s in soup_resource.select(selecting):
            #    print(s)
                for t in s.get_all(tag):
               #     print(t)
                    subarticles["url"] = t.get(attr)
                #    print(t.get(attr))
        except: pass
        return subarticles

    def make_content_folder(self, parent_dir_name):
        if os.path.isdir(parent_dir_name):
            self.remove_dir_tree(parent_dir_name)
        shutil.copytree('./epub-sample', parent_dir_name)

    def image_attach(self, image_url, storage_name):
        try:
            req.urlretrieve(image_url,  storage_name)
            return True
        except: return False

    def html_special_filter(self, string):
        special = ['"', '&', '<', '>', 'ⓒ']
        for i in range(len(special)):
            string = string.replace(special[i], "", 10)
        return string

    def title_filter(self, string):
        string = string.replace("_", " ", 100)
        special_string = ["/", ":", ";", "*", "~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "=", "?", "[", "]", "<",
                          ">", "(", ")", "\n", "\t", "\r", "|"]
        for ss in special_string:
            string = string.replace(ss, "", 10)
    #    print(string)
        return string

    def correctSubtitleEncoding(filename, newFilename, encoding_from, encoding_to='utf-8'):
        with open(filename, 'r', encoding=encoding_from) as fr:
            with open(newFilename, 'w', encoding=encoding_to) as fw:
                for line in fr:
                    fw.write(line[:-1] + '\r\n')


    def get_contents_title_text(self, url, lineoff):
        title = self.title_filter(os.path.basename(url))[:-4]
        body = ""
        file = open(url, 'r', encoding="utf-8")
     #   print(file.encoding)
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
        #        print(line)
                body += "<p>"+line+"</p>"

        file.close()
        return title, body

    def get_contents_title_text_image_order(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = self.title_filter(soup.title.string)
        hs = soup.select('h1')
        hs.append(soup.select('h2'))
        hs.append(soup.select('h3'))
        hs.append(soup.select('h4'))
        texts = soup.select('p')
        texts.append(soup.select('div'))
        images_ = soup.select('img')
     #   print(images_)
        images = []
        for i in images_:
            images.append(i['src'])
        orders = []
        for tag in soup.find_all(True):
            if tag.name == "p" or tag.name == "img" or tag.name == "h1" or tag.name == "h2" or tag.name == "h3" or tag.name == "h4" or tag.name=="div":
                orders.append(tag.name)
                #       print("{0}+{1} = {2} ? {3}".format(len(bodys), len(images), len(orders), len(bodys)+len(images)==len(orders)))
        return title, texts, images, orders

    def get_body(self, contents, dir_name):
        image_tag = False
        body = ""
        for n in range(len(contents)):
            body += "<hr/>"
            body += "<h2 id='item"+str(n)+"' >"+contents[n]['title']+"</h2>\n"
            ran = random.randrange(1000000)
            p, i = 0, 0
            for e in contents[n]['order']:
                if e == 'p':
                    if(image_tag):
                        body += ""
                        image_tag = False
                    else:
                        try:
                            tet = contents[n]['text'][p].text
                        except:
                            tet = contents[n]['text'][p][3:-4]
                        if tet.find(">")>0 or tet.find("<")>0:
                            pass
                        else:
                            body += "<p>"+tet+"</p>"
                    p += 1
                elif e == 'i':
                    http_name = contents[n]['image'][i]
                    if http_name[:4] == "http":
                        if http_name.find(".jpg") or http_name.find(".JPG") > 1:
                            new_name = str(ran)+str(i) + ".jpg"
                        elif http_name.find(".png") or http_name.find(".PNG")> 1:
                            new_name = str(ran)+str(i) + ".png"
                        else:
                            new_name = str(ran)+str(i) + ".gif"
                        if self.image_attach(http_name, dir_name+'/images/'+new_name):
                            body += "<p class='image'><img src='images/"+new_name+"'/></p>\n"
                            image_tag = True
                    i += 1
                else:
                    body += "<"+e+">"+contents[n]['text'][p].text + "</"+e+">\n"
                    p += 1
        return body

    def get_body_for_single(self, contents, dir_name):
        image_tag = False
        body = ""
        ran = random.randrange(1000000)
        p, i = 0, 0
        for e in contents['order']:
            if e == 'p':
                if(image_tag):
                    try: body += "<p>" + contents['text'][p].text + "</p>\n"
                    except: pass
                    image_tag = False
                else:
                #    print(contents['text'][p].text)
                    try:
                        if contents['text'][p].text.find(">")>0 or contents['text'][p].text.find("<")>0: pass
                        else: body += "<p>"+ self.html_special_filter(contents['text'][p].text)+"</p>\n"
                    except: pass
                p += 1
            elif e == 'img':
                try:
                    http_name = contents['image'][i]
                    if http_name[-4:] == '.jpg' or http_name[-4:] == '.JPG' or http_name[-4:] == '.png' or \
                        http_name[-4:] == '.PNG' or http_name[-4:] == '.gif' or http_name[-4:] == '.GIF':
                        new_name = str(ran)+str(i)+http_name[-4:]
                        if self.image_attach(http_name, dir_name+'/images/'+new_name):
                            body += "<p class='image'><img src='images/"+new_name+"'/></p>\n"
                            image_tag = True
                except: pass
                i += 1
            else:
                try: body += "<"+e+">" + self.html_special_filter(contents['text'][p].text) + "</"+e+">\n"
                except: pass
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

    def titlepagehtml(self, title, RANGE):
        return '''<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ko">
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
                <image width="1200" height="1600" xlink:href="'''+RANGE+'''_image.jpg"/>
            </svg>
        </div>
    <p>※주의 : 이 책의 저작권은 ['''+title+''']의 해당 저자들에게 있습니다. 무단복제 및 무단배포할 경우 저작권법에 저촉될 수 있습니다.</p>
        <p>반드시 개인적으로 보아주시기 바랍니다.</p>
    </body>
</html>
        '''

    def tocncx(self, uuid, title, contents, LANGUAGE):
        tocncx = '''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="''' + LANGUAGE + '''">
  <head>
    <meta content="'''+uuid+'''" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="soori (3.14.0)" name="dtb:generator"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>'''+title+'''</text>
  </docTitle>
  <navMap>
      <navPoint id="np1" playOrder="1">
      <navLabel>
        <text>드리는 말씀</text>
      </navLabel>
      <content src="titlepage.xhtml"/>
    </navPoint>
    '''
        for n in range(len(contents)):
            tocncx += '<navPoint id="np'+str(n+2)+'" playOrder="'+str(n+2)+'">\n'
            tocncx += '<navLabel><text>'+contents[n]['title']+'</text></navLabel>\n'
            tocncx += '<content src="index.html#item'+str(n)+'"/></navPoint>'
        tocncx += '''</navMap>
</ncx>'''
        return tocncx

    def tocncx_for_single(self, uuid, contents, LANGUAGE):
        tocncx = '''<?xml version='1.0' encoding='utf-8'?>
        <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="''' + LANGUAGE + '''">
          <head>
            <meta content="''' + uuid + '''" name="dtb:uid"/>
            <meta content="2" name="dtb:depth"/>
            <meta content="soori (3.14.0)" name="dtb:generator"/>
            <meta content="0" name="dtb:totalPageCount"/>
            <meta content="0" name="dtb:maxPageNumber"/>
          </head>
          <docTitle>
            <text>''' + contents['title'] + '''</text>
          </docTitle>
          <navMap>
              <navPoint id="np1" playOrder="1">
              <navLabel>
                <text>드리는 말씀</text>
              </navLabel>
              <content src="titlepage.xhtml"/>
            </navPoint>
            '''
        tocncx += '<navPoint id="np2" playOrder="2">\n'
        tocncx += '<navLabel><text>' + contents['title'] + '</text></navLabel>\n'
        tocncx += '<content src="html.html#item0"/></navPoint>'
        tocncx += '''</navMap>
        </ncx>'''
        return tocncx

    def contentopf(self, uuid, date, time, title, dir_name):
        contentopf = '''<?xml version='1.0' encoding='utf-8'?>
        <package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
        <metadata xmlns:calibre="http://calibre.kovidgoyal.net/2009/metadata" xmlns:dc="http://purl.org/dc/elements/1.1/" 
        xmlns:dcterms="http://purl.org/dc/terms/" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <dc:language>ko</dc:language>
            <meta name="calibre:timestamp" content="''' + str(date) + "T" + str(time) \
                     + '''"/>
            <dc:title> ''' + title + '''</dc:title>
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
        return contentopf


    def make_epub(self, parent_dir_name, title):
        path = pathlib.Path(parent_dir_name).resolve()
        with zipfile.ZipFile(str(title + '.epub'), 'w') as archive:
            archive.write(str(parent_dir_name +'/mimetype'), 'mimetype', compress_type=zipfile.ZIP_STORED)
            for file in path.rglob('*.*'):
            #    print(file)
                archive.write(str(file), str(file.relative_to(path)), compress_type=zipfile.ZIP_DEFLATED)
        self.remove_dir_tree(parent_dir_name)
