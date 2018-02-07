#-*- coding: utf-8 -*-
from datetime import datetime
import random
from core.ToEpubCore import ToEpubCore


class ContentToEpub(ToEpubCore):

    def __init__(self, LANGUAGE, RANGE, URL, LINEOFF):
        self.MakeBook(LANGUAGE, RANGE, URL, LINEOFF)

    def MakeBook(self, LANGUAGE, RANGE, URL, LINEOFF):
        url = URL
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M')
        parent_dir_name = './content'
        dir_name = parent_dir_name + '/OEBPS'
        uuid = "b66f0af5-0fb2-4627-b972-dx"+"{0:10}".format(random.randrange(1, 1000000000))

        self.make_content_folder(parent_dir_name)

        contents = {}
        contents['url'] = URL
        body = ""
        if RANGE == "html":
            contents['title'], contents['text'], contents['image'], contents['order'] = \
                self.get_contents_title_text_image_order(contents['url'])
            body = self.get_body_for_single(contents, dir_name)
        elif RANGE == "text":
            contents['title'], body = self.get_contents_title_text(contents['url'], LINEOFF)

        self.make_file(dir_name + '/titlepage.xhtml', self.titlepagehtml(contents['title'], RANGE))
        self.make_file(dir_name + "/toc.ncx", self.tocncx_for_single(uuid, contents, LANGUAGE))

        html = "<?xml version='1.0' encoding='utf-8'?>\n<html xmlns='http://www.w3.org/1999/xhtml'>\n"
        html += "<head><title>"+contents['title']+"</title></head>\n"
        html += "<body>\n<h1>"+contents['title']+"</h1><p>DATE : "+ date +"</p>"+body+"</body>\n</html>"
        self.make_file(dir_name + "/index.html", html)
        del html

        self.make_file(dir_name + "/content.opf", self.contentopf(uuid, date, time, contents['title'], dir_name))

        #save
        self.make_epub(parent_dir_name, contents['title'])
