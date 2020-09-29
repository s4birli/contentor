import requests
from bs4 import BeautifulSoup

request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Content-Type": "Text",
    "Connection": "keep-alive"
}


def request_url(url):
    return requests.get(url, headers=request_headers)


def get_html(url):
    req = requests.get(url, headers=request_headers)
    return BeautifulSoup(req.content, features="html.parser")


def get_xml(url):
    resp = requests.get(url, headers=request_headers)
    soup = BeautifulSoup(resp.content, features='xml')

    return soup.findAll('item')[0:20]


def get_image(url):
    return requests.get(url, stream=True)
