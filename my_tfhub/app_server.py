# 系统的包
import platform
from flask import Flask, request, Response, current_app, render_template, jsonify
from flask_cors import CORS
from flask_limiter.util import get_remote_address  # pip install Flask-Limiter
from flask_limiter import Limiter
from py_eureka_client import eureka_client
import atexit  # 程序退出 释放资源
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
from loguru import logger
import os

# 自定义包
from app_service import stylization
from app_conf import GConfig
from baidu_service import ImageService, TextService
from app_utils import img_to_base64

# // r'/*' 是通配符，让本服务器所有的 URL 都允许跨域请求

# 全局配置设置
app = Flask(__name__)

app.config["INFO"] = True

conf = GConfig()

limite = Limiter(app, default_limits=['8/minute', '30/hour', '50/day'], key_func=get_remote_address)

'''
第一个请求过来之前，启动browser资源池，以后每个请求会在资源池里拿资源，减少browser启动时间。
'''


def setEureka():
    server_host = conf.SERVER_CONFIG['host']
    server_port = int(conf.SERVER_CONFIG['port'])
    eureka_client.init(eureka_server="http://modderbug.cn:8080/eureka/",
                       app_name="tfhub_server",
                       # 当前组件的主机名，可选参数，如果不填写会自动计算一个，如果服务和 eureka 服务器部署在同一台机器，请必须填写，否则会计算出 127.0.0.1
                       instance_host=server_host,
                       instance_port=server_port,
                       # 调用其他服务时的高可用策略，可选，默认为随机
                       # ha_strategy=eureka_client.HA_STRATEGY_RANDOM
                       )


# setEureka()


@app.before_first_request
def init():
    current_app.logger.info('----init before_first_request --')
    global image_service
    image_service = ImageService()
    global text_service
    text_service = TextService()


@atexit.register
def f():
    print('结束')


# 默认显示 图片，加载失败即不可用
@app.route('/img_test')
@limite.exempt
def hello_world3():
    from io import BytesIO
    img = Image.open('images/1.jpg', "r")
    figfile = BytesIO()
    img.save(figfile, format='JPEG')
    return Response(response=figfile.getvalue(), status=200, mimetype="image/jpeg", headers={"Session": "ok"})


@app.route('/img_plus', methods=['POST'])
def img_plus():
    """
    图片放大
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)
    res = image_service.image_plus(img_base64)

    if res.get("error_code", "") != "":
        return jsonify(res)
    return Response(response=res['image'], status=200, mimetype="image/png")


@app.route('/img_waifu/<mask_id>', methods=['POST'])
def img_waifu(mask_id):
    """
    图片二次元
    :param mask_id: 口罩类别，0为无
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)
    if int(mask_id) == 0:
        res = image_service.image_waifu(img_base64)
    else:
        res = image_service.image_waifu(img_base64, "anime_mask", mask_id)
    return Response(response=res['image'], status=200, mimetype="image/png")


@app.route('/img_transtyle/<style_label>', methods=['POST'])
def img_transtyle(style_label):
    """
    图片风格转化，非风格迁移
    :param mask_id: 口罩类别，0为无
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)
    res = image_service.image_stylization(img_base64, style_label)
    if res.get("error_code", "") != "":
        return jsonify(res)
    return Response(response=res['image'], status=200, mimetype="image/png")


@app.route('/img_colorful', methods=['POST'])
def img_colorful():
    """
    图片上色
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)
    res = image_service.image_colorful(img_base64)
    if res.get("error_code", "") != "":
        return jsonify(res)
    return Response(response=res['image'], status=200, mimetype="image/png")


@app.route('/img_definition', methods=['POST'])
def img_definition():
    """
    图片清晰度增强
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)
    res = image_service.image_definition(img_base64)
    if res.get("error_code", "") != "":
        return jsonify(res)
    return Response(response=res['image'], status=200, mimetype="image/png")


@app.route('/txt_recognize/<type_label>', methods=['POST'])
def txt_recognize(type_label):
    """
    图片清晰度增强
    :return:
    """
    upload_files = request.files.getlist('file')
    img_base64 = img_to_base64(upload_files)

    if type_label == 'normal':
        res = text_service.text_recognize(img_base64)
    elif type_label == 'plus':
        res = text_service.text_recognize_plus(img_base64)
    elif type_label == 'written':
        res = text_service.text_recognize_written(img_base64)
    else:
        res = text_service.text_recognize(img_base64)

    if res.get("error_code", "") != "":
        return jsonify(res)
    return jsonify(res)


@app.route('/post_style', methods=['POST'])
def post_style():
    """
    传入两张图片 返回转换后图片
    :return:
    """
    res = None
    upload_files = request.files.getlist('file')
    for file in upload_files:
        filename = secure_filename(file.filename)
        logger.info(filename)
    img1 = Image.open(upload_files[0])
    img2 = Image.open(upload_files[1])
    img, base64 = stylization(np.array(img1), np.array(img2))
    return Response(response=base64, status=200, headers={"Session": "ok"})


@app.route('/')
def hello_world():
    return Response(response="backend started success ! ", status=200, mimetype="application/json")


@app.route('/share')
def share_file():
    l = os.listdir('static')
    s = []
    for i in l:
        s.append("http://" + conf.SERVER_CONFIG['host'] + ":" + conf.SERVER_CONFIG['port'] + '/static/' + i)
    # return Response(response=s, status=200, mimetype="application/json")

    return render_template('html/index.html', seq=s,name=l)


@app.route('/test')
def hello_world2():
    return render_template('html/index_old.html')


if __name__ == '__main__':
    print(platform.system().lower())
    CORS(app, resources=r'/*')
    if os.path.exists(conf.get('ssl', 'pem')) and os.path.exists(conf.get('ssl', 'key')):
        app.run(host=conf.SERVER_CONFIG['host'], port=conf.SERVER_CONFIG['port'],
                threaded=True)  # app.run(0.0.0.0, 8000, debug, options)
    else:
        logger.warning("server start without SSL !")
        app.run(host=conf.SERVER_CONFIG['host'], port=conf.SERVER_CONFIG['port'],
                threaded=True)  # app.run(0.0.0.0, 8000, debug, options)
