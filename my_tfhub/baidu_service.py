import requests
from loguru import logger
import os
from PIL import Image
from app_conf import GConfig
import json
import base64

conf = GConfig()


class ImageService(object):
    def __init__(self):
        client_credentials = conf.BAIDU_API['grant_type']
        ak = conf.BAIDU_API['ak']
        sk = conf.BAIDU_API['sk']
        url = conf.BAIDU_API['url'] + "?" + \
              "grant_type=" + client_credentials + "&" + \
              "client_id=" + ak + "&" + \
              "client_secret=" + sk
        res_token = requests.get(url)
        token_json = res_token.json()
        self.access_token = token_json['access_token']
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

    def image_plus(self, img):
        """
        图片无损放大
        :return:
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_quality_enhance"
        params = {"image": img}
        request_url = request_url + "?access_token=" + self.access_token
        response = requests.post(request_url, data=params, headers=self.headers)
        return response.json()

    def image_colorful(self, img):
        """
        黑白图像上色
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/colourize"
        params = {"image": img}
        request_url = request_url + "?access_token=" + self.access_token
        response = requests.post(request_url, data=params, headers=self.headers)
        return response.json()

    def image_stylization(self, img, style_label):
        """
        图像风格转换
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/style_trans"

        params = {"image": img, "option": style_label}
        request_url = request_url + "?access_token=" + self.access_token

        response = requests.post(request_url, data=params, headers=self.headers)
        return response.json()

    def image_waifu(self, img, type_id="anime", mask_id="1"):
        """
        人像动漫化
        """

        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
        params = {"image": img, "type": type_id, "mask_id": mask_id}
        request_url = request_url + "?access_token=" + self.access_token

        response = requests.post(request_url, data=params, headers=self.headers)
        if response.json().get("error_code", "") != "":
            logger.error(response.json())
        return response.json()

    def image_definition(self, img):
        """
        图像清晰度增强
        """
        request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/image_definition_enhance"
        # 二进制方式打开图片文件
        params = {"image": img}
        request_url = request_url + "?access_token=" + self.access_token
        response = requests.post(request_url, data=params, headers=self.headers)

        return response.json()


class TextService(object):
    def __init__(self):
        client_credentials = conf.BAIDU_API['grant_type']
        ak = conf.get("baidu_api", "text_ak")
        sk = conf.get("baidu_api", "text_sk")
        url = conf.BAIDU_API['url'] + "?" + \
              "grant_type=" + client_credentials + "&" + \
              "client_id=" + ak + "&" + \
              "client_secret=" + sk
        res_token = requests.get(url)
        token_json = res_token.json()
        self.access_token = token_json['access_token']
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}

    def text_recognize(self, img):
        '''
        通用文字识别
        '''
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
        params = {"image": img}
        request_url = request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        return response.json()

    def text_recognize_plus(self, img):
        '''
        通用文字识别（高精度版）
        '''

        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"

        params = {"image": img}

        request_url = request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        return response.json()

    def text_recognize_written(self, img):
        '''
        手写文字识别
        '''

        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting"
        # 二进制方式打开图片文件

        params = {"image": img}

        request_url = request_url + "?access_token=" + self.access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        return response.json()

# service = BaiduService()
# base64_str = service.image_plus()
# base64_str = service.image_definition()
# base64_str = service.image_waifu()

# # 二进制方式打开图片文件
# f = open(r'C:\Users\wuxiaowei_a\PycharmProjects\my_tfhub\images\1.jpg', 'rb')
# img = base64.b64encode(f.read())

# with open(r'C:\Users\wuxiaowei_a\PycharmProjects\my_tfhub\images\1_d+.jpg', 'wb') as f:
#     f.write(base64.b64decode(base64_str))


if __name__ == '__main__':
    ser = TextService()
    # f = open(r'C:\Users\wuxiaowei_a\Pictures\未命名1610355281.png', 'rb')
    f = open(r'C:\Users\wuxiaowei_a\Pictures\u=3722356994,2795839394&fm=26&gp=0.jpg', 'rb')
    img = base64.b64encode(f.read())
    # res = ser.text_recognize(img)
    # res2 = ser.text_recognize_plus(img)
    res3 = ser.text_recognize_written(img)
    # print(res)
    # print(res2)
    print(res3)
