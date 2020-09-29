from bson import ObjectId
from constractor import *
import test
import remover


def main():
    try:
        remover.remove_images()
        data = db()
        url_active_list = data.get_active_urls()
        for url in url_active_list:
            print("url: " + str(url['_id']))
            reqs = data.get_requests_active(ObjectId(url['_id']))
            for req in reqs:
                run(url, req)

            data.updateLastUpdate(url)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
