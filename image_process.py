from optimization_image import image_optimize, isJPEG
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from request import get_image
from datetime import date
from PIL import Image
import os
import uuid
import mimetypes
import time



def upload_image(url, news_item):
    try:
        image_url = news_item['image_url']
        uuid_txt = str(uuid.uuid1()).replace("-", "").upper()

        # Download File
        img_data = get_image(news_item['image_url'])
        file_name = "{}.{}".format(uuid_txt, image_url.split('/')[-1].split('.')[1])
        file_path = "{}\\{}".format(os.getcwd(), file_name)
        with open(file_path, 'wb') as handler:
            handler.write(img_data.content)

        # convert image to jpg
        img_type = isJPEG(file_path)
        if img_type is False:
            im = Image.open(file_path)
            rgb_im = im.convert('RGB')
            file_path = "{}\\{}.{}".format(os.getcwd(), uuid_txt, "jpg")
            rgb_im.save(file_path)

        # Optimize
        image_optimize(file_path)

        # get minetype
        mimetypes = get_mimetypes(file_name)

        return upload_media(url, file_path, news_item['title'], news_item['title'], news_item['spinnedText'][:100], mimetypes)
    except Exception as e:
        print(e)


def get_mimetypes(file_name):
    try:
        _res = mimetypes.read_mime_types(file_name)
        return _res
    except:
        pass

    try:
        _res = mimetypes.guess_type(file_name)[0]
        return _res
    except:
        pass

    return None


def upload_media(url, path, file_name, title, desc, type):
    try:
        today = date.today()
        _url = "{}/{}".format(url.get('url'), "xmlrpc.php")
        user_name = url.get('userName')
        password = url.get('password')
        client = Client(_url, user_name, password)

        data = {
            'name': file_name[:10] + " " + today.strftime("%d%m%y"),
            'type': type,  # mimetype
            'caption': title[0:20],
            'description': desc
        }

        with open(path, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = client.call(media.UploadFile(data))
        return response

    except Exception as e:
        print(e)
        return None
