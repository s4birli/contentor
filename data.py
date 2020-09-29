from pymongo import MongoClient
from bson import ObjectId
import datetime
import configparser


class data:
    def __init__(self):

        config = configparser.ConfigParser()
        res = config.read('config.ini')
        conn = str(config['DEFAULT']['connection_string'])
        self.client = MongoClient(conn)
        self.db = self.client.ContentorDb

    def get_active_urls(self):
        return self.db.Urls.find({'isActive': True})

    def get_urls(self):
        return self.db.Urls

    def get_url_by_id(self, _id):
        query = {"_id": ObjectId(_id)}
        return self.db.Urls.find_one(query)

    def get_requests(self, url_id):
        return self.db.Requests.find({'urlId': url_id})

    def update_request_item(self, news_item):
        self.db.RequestItems.update_one({'guid': news_item.get('guid')}, {"$set": {"postId": news_item.get('postId')}})

    def get_latest_post(self, request):
        return self.db.RequestItems.find_one({"isPublished": True, 'category': request.get('category')}, {'orderby': 'post_date', 'order': 'DESC', 'title': 1, 'link': 1, 'postId': 1, '_id': 0})

    def get_requests_active(self, url_id):
        return self.db.Requests.find({'urlId': url_id, 'isActive': True})

    def updateLastUpdate(self, url):
        #url_item = self.get_url_by_id(url.get("_id"))
        self.db.Urls.update_one({"_id": ObjectId(url.get("_id"))}, {"$set": {"lastUpdate": datetime.datetime.now()}})

    def exist(self, news_item):
        return self.db.RequestItems.find(news_item).count() == 0

    def add_request_items(self, news_item):
        req_items = self.db.RequestItems.find_one({'guid': news_item.get('guid')})
        if req_items is None:
            self.db.RequestItems.insert(news_item)

    def find_request(self, news_item):
        return self.db.RequestItems.find_one(news_item)

    def request_update(self, news_item):
        self.db.RequestItems.update_one(news_item, {"$set": {"isPublished": True}})

    def get_forbidden_words(self):
        return self.db.ForbiddenWords.find()

    def get_forbidden_url_words(self):
        return self.db.ForbidenUrlWords.find({}, {"value": 1, "_id": 0})

    def remove_news_item(self, guid):
        self.db.RequestItems.delete_one({'guid': guid})


def db():
    return data()
