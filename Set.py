import json
import sys

# 绝对路径
import frozen_dir


# 读取cookie文件
def load_cookie():
    file = open(frozen_dir.app_path() + '/Set/cookie.txt', mode='r', encoding='utf-8')
    file_txt = file.read()
    file.close()
    return file_txt