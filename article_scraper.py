from newspaper import Article


def get_article(url):
    try:
        _url = url.strip()
        article = Article(_url, language='en')
        article.download()
        article.parse()

        try:
            article.nlp()
        except:
            pass

        return article
    except Exception as e:
        print(e)
        return None
