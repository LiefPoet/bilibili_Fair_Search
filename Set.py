import json
import os
import sys
from tkinter.messagebox import showinfo

# 绝对路径
import frozen_dir


# 读取cookie文件
def load_cookie():
    file = open(frozen_dir.app_path() + '/Set/cookie.txt', mode='r', encoding='utf-8')
    file_txt = file.read()
    file.close()
    return file_txt

def load_URL():
    file = open(frozen_dir.app_path() + '/Set/链接地址.txt', mode='r', encoding='utf-8')
    URL_txt = file.read()
    file.close()
    return URL_txt

# 打开cookie文本
def write_Cookie():
    try:
        file = frozen_dir.app_path() + "/Set/cookie.txt"
        os.startfile(file)
    except Exception as e:
        showinfo(title='错误异常', message=f'{e}')

# 打开链接地址
def write_URL():
    try:
        file = frozen_dir.app_path() + "/Set/链接地址.txt"
        os.startfile(file)
    except Exception as e:
        showinfo(title='错误异常', message=f'{e}')



# 本地根目录创建文件夹
def file_folder(text):
    try:
        save_path = frozen_dir.app_path() + fr"/Set/item/"
        if os.path.exists(save_path + f'{text}.txt'):
            print(f'文件{save_path}存在')
        else:
            # 创建一个txt文件并写入内容
            file = open(save_path + f"{text}.txt", "w")
            file.close()
    except Exception as e:
        showinfo(title='错误异常', message=f'{e}')
