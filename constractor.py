from request import get_xml
from remover import clean_title, reformat_text, add_internal_link, corrected_sub_tag
from data import db
from SpinRewritter import get_spinned
from article_scraper import get_article
from wordpress import publish_article


def run(url, req):
    try:
        data = db()
        xml_item = get_xml(req['url'])
        for item in xml_item:
            if "/transfer-centre" in item.link.text:
                continue

            guid = item.guid.text if item.guid is not None else item.link.text
            link = item.comments.text.replace("#respond", "") if ".google.com" in item.link.text else item.link.text

            try:
                news_item = {'guid': guid}
                title = clean_title(item.title.text)
                result = False

                if data.exist(news_item):
                    news_item['urlId'] = url.get('_id')
                    article = get_article(link)

                    if article is None:
                        continue

                    if len(article.text) < url.get('wordCount'):
                        continue

                    news_item['originalText'] = article.text
                    news_item['link'] = link

                    article.text = reformat_text(link)
                    full_context = get_spinned("{} || {}".format(title, article.text))

                    if full_context is None:
                        print('full_context is None')
                        continue

                    title = full_context.split("||")[0].strip()
                    article.text = full_context.split("||")[1].strip()

                    article.keywords.append("Hot News")
                    article.text = corrected_sub_tag(article.text)
                    desc = article.meta_description if len(article.meta_description) > 0 else article.text[:150]
                    news_item['postId'] = ''
                    news_item['title'] = title
                    news_item['pubdate'] = item.pubDate.text
                    news_item['requestsId'] = req.get('_id')
                    news_item['category'] = req.get('category')
                    news_item['image_url'] = article.top_image.replace("/branded_news/", "/cpsprodpb/")
                    news_item['description'] = desc
                    news_item['isPublished'] = False
                    news_item['keywords'] = article.keywords
                    news_item['spinnedText'] = add_internal_link(url, req, article.text)
                    data.add_request_items(news_item)
                    result = publish_article(url, news_item)
                else:
                    news_item = data.find_request(news_item)
                    if news_item["isPublished"] is False:
                        result = publish_article(url, news_item)

                if result is True:
                    data.request_update(news_item)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
