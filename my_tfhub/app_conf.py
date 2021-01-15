#!/usr/bin/env python3
# coding: utf-8
# 配置文件
import os
import configparser
import sys
from loguru import logger


# import redis
# import pymysql


class GConfig(object):  # 生产环境
    def __init__(self):
        app_env = get_env()
        self.conf = configparser.SafeConfigParser()
        self.conf_file = self.conf.read('conf/' + app_env + '.conf', encoding='utf-8')
        if not self.conf_file:
            logger.warning("没有读取到配置文件，使用默认的配置文件！")
            self.conf_file = self.conf.read("conf/dev.conf")
        if not self.conf_file:
            exit("dev|prod|default.conf 没有找到，请将文件放入项目目录！")

        # self.BASE_PATH = self.conf.get('app', 'base_path')
        # self.EXECUTABLE_PATH = self.conf.get('app', 'executable_path')
        # self.USER_AGENT = self.conf.get('app', 'UserAgent')
        # self.BROWSER_HEIGHT = int(self.conf.get('app', 'browser_height'))
        # self.BROWSER_WIDTH = int(self.conf.get('app', 'browser_width'))

        self.SERVER_CONFIG = {
            'port': self.conf.get('app', 'server_port'),
            'host': self.conf.get('app', 'server_host')
        }

        self.BAIDU_API = {
            "url": self.conf.get('baidu_api', 'url'),
            "grant_type": self.conf.get('baidu_api', 'grant_type'),
            "client_id": self.conf.get('baidu_api', 'client_id'),
            "client_secret": self.conf.get('baidu_api', 'client_secret'),
            "ak": self.conf.get('baidu_api', 'image_ak'),
            "sk": self.conf.get('baidu_api', 'image_sk')
        }

    def get(self,section,option):
        return self.conf.get(section,option)


def get_env():
    if os.environ.get('APP_ENV'):
        app_env = os.environ.get('APP_ENV')
        logger.warning("使用环境变量加载配置文件：" + 'env ' + app_env)
        return app_env
    else:
        num = len(sys.argv)  # 参数个数
        if num != 2:
            exit("参数错误,必须传环境变量!比如: python xx.py dev|prod|default")
        env = sys.argv[1]  # 环境
        app_env = os.environ.get('APP_ENV', env).lower()
        logger.warning("使用参数加载配置文件：" + 'args ' + app_env)
        return app_env


if __name__ == '__main__':
    a = GConfig()
    print(a.MYSQL_CONFIG)
    print(a.REDIS_CONFIG)
    print(a.SERVER_CONFIG)
    print(a.BASE_PATH)
    print(a.EXECUTABLE_PATH)
    print(a.USER_AGENT)
    print('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

    # redis_con = redis.Redis(**a.REDIS_CONFIG, decode_responses=True)
    # print(redis_con.keys('*'))
    #
    # a.MYSQL_CONFIG['port'] = int(a.MYSQL_CONFIG['port'])
    # con = pymysql.connect(**a.MYSQL_CONFIG)
