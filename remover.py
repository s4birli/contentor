from request import get_html
from optimization_image import isImage
from newspaper import fulltext
from data import db
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
import re
import time
import collections
import os


def remove_images():
    try:
        for file_path in os.listdir():
            if isImage(file_path):
                os.remove(file_path)
    except OSError as e:
        details = 'Error while removing temporary file.'


def get_focus(title, tags):
    focus = ""
    try:
        for tag in tags:
            for title in title.split(' '):
                if tag == title:
                    focus = focus + " " + tag
    except Exception as e:
        print(e)

    return focus


def clean_title(title):
    title = title.replace("CNET", "")
    title = title.replace("-", "")
    return title.strip()


def reformat_text(link):
    try:
        soup = get_html(link)
        try:
            soup.find('figure').decompose()
            soup.find('img').decompose()
        except:
            pass

        text = fulltext(str(soup.currentTag))
        text = replace_texts(text)
        text = clean_url(text)
        text = clean_email(text)
        return add_sub_title(soup, text)
    except Exception as e:
        print(e)
        pass


def replace_texts(text):
    data = db()
    get_forbidden_words = data.get_forbidden_words()
    for word in get_forbidden_words:
        text = text.replace(word['value'], "")
    return text


def get_combination(text):
    try:
        data = db()
        get_forbidden_url_words = data.get_forbidden_url_words()

        for forbidden in get_forbidden_url_words:
            text = re.sub(forbidden["value"], "", text, 5000000)

        lines = re.split("\n", text)
        combinations = []

        for line in lines:
            x = re.split(" ", line.strip())
            words = []
            for i in range(len(x)):
                if len(x[i].strip()) > 3 and {"value": x[i].strip()} not in get_forbidden_url_words:
                    words.append(x[i])
                else:
                    continue

            for i in range(len(words) - 1):
                if len(words[i].strip()) > 0:
                    combinations.append(words[i] + " " + words[i + 1])

        Counter = collections.Counter(combinations)
        return Counter.most_common(len(combinations))
    except Exception as e:
        print(e)
        return None


def get_mostCommon(text1, text2):
    list1 = get_combination(text1)
    list2 = get_combination(text2)
    return_item = ""
    for first in list1:
        for second in list2:
            if first[0] == second[0]:
                return_item = first[0]
                break
    if len(return_item) == 0:
        return_item = list2[0][0]

    return return_item


def get_post(url):
    try:
        _url = "{}/{}".format(url.get('url'), "xmlrpc.php")
        user_name = url.get('userName')
        password = url.get('password')
        client = Client(_url, user_name, password)
        news = client.call(posts.GetPosts({'orderby': 'date', 'order': 'DESC'}))
        if news is None:
            return None
        else:
            return news[0]
    except Exception as e:
        print(e)
        return None


def add_internal_link(url, request, text):
    try:

        previous_post = get_post(url)
        if previous_post is None:
            return None

        title = previous_post.title
        search_text = get_mostCommon(title, text)
        original_text = text
        replace_text = '<a href="{}" target="_self">{}</a>'.format(previous_post.link, search_text)
        return re.sub(search_text, replace_text, original_text, 1)
    except Exception as e:
        print(e)
        return None


def add_sub_title(soup, text):
    try:
        for i in ['2', '3', '4']:
            for sub in soup.find_all(['h' + i]):
                original_text = text
                search_text = sub.text
                replace_text = '[h{}]{}[/h{}]'.format(i, search_text, i)
                sub_text = re.sub(search_text, replace_text, original_text, 1)
                text = sub_text
    except Exception as e:
        print(e)

    return text


def corrected_sub_tag(text):
    for i in ['2', '3', '4']:
        match_list = re.findall(r"^(\[h.+" + i + "+\])$", text, re.MULTILINE)
        for match in match_list:
            original_text = match
            replace_text = match.replace("[h" + i, "<h" + i)
            replace_text = replace_text.replace("[/h" + i, "</h" + i)
            replace_text = replace_text.replace("]", ">")
            ##replace_text = match.replace("[" + i + "]", "<h" + i + ">").replace("[/" + i + "]", "</h" + i + ">")
            text = text.replace(original_text, replace_text)

    return text


def clean_email(text):
    return re.sub(r"\S*@\S*\s?", "", text, flags=re.MULTILINE)


def clean_url(text):
    return re.sub(r"http\S+", "", text, flags=re.MULTILINE)


def clean_image_text_old(soup, text):
    original_text = text
    try:
        for img in soup.find_all('figure'):
            sub_text = re.sub(img.text, "", original_text, 1)

            words = re.split("\n", img.text)

            sub_text = re.sub(img.text, "", original_text, 1)
            original_text = sub_text

    except Exception as e:
        print(e)
    return original_text


def clean_image_text(soup, text):
    try:
        for img in soup.find_all('figure'):
            sub_text = re.sub("\n", " ", img.text, 50)
            replace_txt = ""
            for txt in sub_text.split(" "):
                if len(txt) > 0:
                    replace_txt = replace_txt + " " + txt.strip()

            replace_txt = replace_txt.strip()
            if len(replace_txt.strip()) > 0:
                original_text = text
                sub_text = ""
                for txt in replace_txt.split(" "):
                    if len(txt) > 0:
                        sub_text = re.sub(txt, "", original_text, 1)
                        original_text = sub_text.strip()

                text = original_text
    except Exception as e:
        print(e)
    return text


def remove_image(link):
    try:
        time.sleep(5)
        article_soup = get_html(link)
        article_soup.find('figure').decompose()
        return fulltext(str(article_soup.currentTag))
    except Exception as e:
        pass
