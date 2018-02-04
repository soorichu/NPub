import requests
from bs4 import BeautifulSoup
import NewsTags

def test1():
    newstag = NewsTags.NewsTag
    print(newstag)

def test2(http_string):
    response = requests.get(http_string)
    soup = BeautifulSoup(response.content, "html.parser")
    print(len(soup.find_all('item')))


test2("http://www.ktimes.com/www/rss/rss.xml")