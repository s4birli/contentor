import base64

from newspaper import fulltext
import requests
from html.parser import HTMLParser
from article_scraper import get_article

import requests
import json


##test.connect()
##print(newspaper.hot())
##print(newspaper.popular_urls())
##print(newspaper.languages())
##a = Article('https://techcrunch.com/2020/09/24/heres-everything-amazon-announced-at-its-latest-hardware-event/', keep_article_html=True)
##a.download()
##a.parse()

##print(a.article_html)
##print(a.url)
##print('')
# test.test_method("https://www.bbc.co.uk/news/business-54264689")
# url_list = data.get_urls()

def connect():
    try:
        user = 'Umut'
        pythonapp = 'gat0 iPib 3IGr bv8I 8GvN GdWa'
        url = 'https://wiredaccount.com/wp-json/wp/v2'

        token = str(base64.standard_b64encode((user + ':' + pythonapp).encode("utf-8")))




        headers = {'Authorization': 'Basic ' + token}

        post = {'date': '2017-06-19T20:00:35',
                'title': 'First REST API post',
                'slug': 'rest-api-1',
                'status': 'publish',
                'content': 'this is the content post',
                'author': '1',
                'excerpt': 'Exceptional post!',
                'format': 'standard'
                }
        r = requests.post(url + '/posts', headers=headers, json=post)
        print('Your post is published on ' + json.loads(r.content)['link'])
    except Exception as e:
        print(e)


def test_method(url):
    article = get_article(url)
    req = requests.get(url).text
    tst = req.parse()
    parser = MyHTMLParser()
    tst = parser.feed(req)

    text = fulltext(req)


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)



def get_last_post(url, req):
    try:
        _url = "{}/{}".format(url.get('url'), "xmlrpc.php")
        user_name = url.get('userName')
        password = url.get('password')
        #client = Client(_url, user_name, password)
        query = {'category': req.get('category')}
        #news = client.call(posts.GetPosts({}))
        #return news[0]
    except Exception as e:
        print(e)
        return None