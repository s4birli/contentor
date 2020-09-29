from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from image_process import upload_image
import remover
from data import db


def get_client(url):
    _url = "{}/{}".format(url.get('url'), "xmlrpc.php")
    user_name = url.get('userName')
    password = url.get('password')
    return Client(_url, user_name, password)


def publish_article(url, news_item):
    try:
        data = db()
        if news_item["spinnedText"] is None:
            data.remove_news_item(news_item.get('guid'))
            return False

        attachment = upload_image(url, news_item)

        focus = remover.get_focus(news_item.get('title'), news_item.get('keywords'))

        yoast = [{'key': '_yoast_wpseo_opengraph-title', 'value': news_item.get('title')},
                 {'key': '_yoast_wpseo_twitter-title', 'value': news_item.get('title')},
                 {'key': 'post-feature-caption', 'value': news_item.get('title')},
                 {'key': 'twitterCardType', 'value': 'summary_large_image'},
                 {'key': '_yoast_wpseo_focuskw', 'value': focus},
                 {'key': 'sub-title', 'value': news_item.get('spinnedText')[:215]},
                 {'key': 'meta_description', 'value': news_item.get('spinnedText')[:215]},
                 {'key': 'mt_description', 'value': news_item.get('spinnedText')[:215]}]

        if attachment is not None:
            yoast.append({'key': 'cardImage', 'value': attachment['url']})

        remover.replace_texts(news_item.get('spinnedText'))

        post = WordPressPost()
        post.title = news_item.get('title')
        post.content = news_item.get('spinnedText')
        post.terms_names = {'post_tag': news_item.get('keywords'), 'category': news_item.get('category')}
        post.post_status = 'publish'
        if attachment is not None:
            post.thumbnail = attachment['id']

        post.custom_fields = yoast
        client = get_client(url)
        post.id = client.call(posts.NewPost(post))
        news_item['postId'] = post.id
        data.update_request_item(news_item)
        remover.remove_images()

        return True
    except Exception as e:
        print(e)
        return False
