import base64
import os
import threading
from time import sleep

import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import Set
import frozen_dir
import icon

url = "https://mall.bilibili.com/mall-magic-c/internet/c2c/v2/list"
#url = "https://mall.bilibili.com/neul-next/index.html?page=magic-market_index"

def ALL_Window():
    # 定义一个窗口程序
    My_Window = tk.Tk()
    # 窗口的标题显示名
    My_Window.title('魔力赏搜索')
    # 窗口的大小
    My_Window.geometry('450x510')
    # 窗口颜色
    My_Window.config(background='#333333')
    # 得到屏幕宽度
    sw = My_Window.winfo_screenwidth()
    # 得到屏幕高度
    sh = My_Window.winfo_screenheight()
    ww = 450
    wh = 510
    x = (sw - ww) / 2
    y = (sh - wh) / 2
    My_Window.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
    # 窗口不可调节大小
    My_Window.resizable(False, False)
    # 添加程序图标
    icon1 = icon.Icon
    # 获取改ig变量的内容
    icc = icon1().ig
    with open('tmp.ico', 'wb') as tmp:
        tmp.write(base64.b64decode(icc))
    # 创建一个临时ico图标给程序使用
    My_Window.iconbitmap('tmp.ico')
    # 最后删除该文件
    os.remove('tmp.ico')

    #打折力度
    def iscount_Combobox_Get():
        # 当改变值时 执行
        discountBox_txt = discount_Combobox.get()
        if discountBox_txt == "默认不选择":
            discount_Text = 'null'
        elif discountBox_txt == "3折以下":
            discount_Text = "0-30"
        elif discountBox_txt == "3-5折":
            discount_Text = "30-50"
        elif discountBox_txt == "5-7折":
            discount_Text = "50-70"
        elif discountBox_txt =='7折以上':
            discount_Text = '70-100'
        return discount_Text

    # 按排序规则搜索
    def SortType():
        sorttype = arrangement_Combobox.get()
        if sorttype == "综合搜索":
            SortType_Text = "TIME_DESC"
        elif sorttype == "价格升序搜索":
            SortType_Text = "PRICE_ASC"
        elif sorttype == "价格降序搜索":
            SortType_Text = "PRICE_DESC"
        return SortType_Text

    # 按种类规则搜索
    def variety_item():
        sorttype = variety_item_Combobox.get()
        if sorttype == "手办":
            variety_item_Text = "2312"
        elif sorttype == "模型":
            variety_item_Text = "2066"
        elif sorttype == "周边":
            variety_item_Text = "2331"
        elif sorttype == "3C":
            variety_item_Text = "2273"
        elif sorttype == "福袋":
            variety_item_Text = "fudai_cate_id"
        return variety_item_Text

    '''
        #是否仅输出一位搜索结果
        def one_print():
            one_print_ = one_print_Combobox.get()
            if one_print_ == '是':
                one_print_Text = True
            elif one_print_ == '否':
                one_print_Text = False
            return one_print_Text
            def click_Forced_Termination():
        pass
    '''

    def Money(money):
        itme_money=int(money)*100
        return itme_money
    # 搜索主逻辑代码
    def search_lock():
        """
        简单的问候函数。

        参数:
            item:查询物品名称

            priceFilters:最大最小价格

            discountFilters: 打折力度

            categoryFilter:物品代码

            sortType:排序规则
        """
        cookie = f"{Set.load_cookie()}"
        i_want = []
        # 锁定按钮
        Srarch_Button.state(['disabled'])
        Srarch_txt.state(['disabled'])
        Maximum_Price_txt.state(['disabled'])
        Minimum_Price_txt.state(['disabled'])
        nextId = None
        while True:
            if iscount_Combobox_Get() != 'null':
                payload = json.dumps({
                    "categoryFilter": str(variety_item()),
                    "priceFilters": [
                        str(Money(Minimum_Price_txt.get())) + "-" + str(Money(Maximum_Price_txt.get()))
                    ],
                    "discountFilters": [
                         str(iscount_Combobox_Get())
                    ],
                    "nextId": nextId,
                    "sortType": str(SortType())
                })
            else:
                payload = json.dumps({
                    "categoryFilter": str(variety_item()),
                    "priceFilters": [
                        str(Money(Minimum_Price_txt.get())) + "-" + str(Money(Maximum_Price_txt.get()))
                    ],
                    "nextId": nextId,
                    "sortType": str(SortType())
                })

            headers = {
                'authority': 'mall.bilibili.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,ja;q=0.4',
                'content-type': 'application/json',
                'cookie': cookie,
                'origin': 'https://mall.bilibili.com',
                'referer': 'https://mall.bilibili.com/neul-next/index.html?page=magic-market_index',
                'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
            }
            try:
                response = requests.request("POST", str(Set.load_URL()), headers=headers, data=payload)
                print_txt = response.text
                print_Label.config(justify="left", anchor="w", text=f'运行代码：\n{print_txt}\n', wraplength=370)
                response = response.json()
                #解析网站源码
                soup = BeautifulSoup(print_txt, 'html.parser')
                #查找是否拥有风控报错信息
                Forced_termination = soup.find('div',class_ = "error-container")
                #print('目前列表选项：',Forced_termination)
                #自动终止程序
                if Forced_termination != None :
                    # 自动创建对应搜索物品
                    item_ALL(Srarch_txt.get())
                    # 找到物品弹窗
                    showinfo(title='搜索结果',message='程序已自动终止运行!\n已经风控！\n输出当前全部搜索结果\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    Srarch_Button.state(['!disabled'])
                    Srarch_txt.state(['!disabled'])
                    Maximum_Price_txt.state(['!disabled'])
                    Minimum_Price_txt.state(['!disabled'])
                    break
                elif int(Forced_termination_Scale.get()) >= 5:
                    # 自动创建对应搜索物品
                    item_ALL(Srarch_txt.get())
                    # 找到物品弹窗
                    showinfo(title='搜索结果',message='程序已手动终止运行!\n输出当前全部搜索结果\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    Srarch_Button.state(['!disabled'])
                    Srarch_txt.state(['!disabled'])
                    Maximum_Price_txt.state(['!disabled'])
                    Minimum_Price_txt.state(['!disabled'])
                    #滑块归位
                    Forced_termination_Scale.set(0)
                    break

                # 拿到翻页的变量
                nextId = response["data"]["nextId"]
                if nextId is None:
                    if i_want == []:
                        # 未找到物品弹窗
                        showinfo(title='搜索结果', message='未能在规定区间找到所选物品\n请扩大搜索区间或检查搜索名称')
                        # 解锁按钮
                        Srarch_Button.state(['!disabled'])
                        Srarch_txt.state(['!disabled'])
                        Maximum_Price_txt.state(['!disabled'])
                        Minimum_Price_txt.state(['!disabled'])
                        break

                    print("+++++++++++++++++++++")
                    print(i_want)
                    print("=========================")
                    min_element = min(i_want, key=lambda x: x["showPrice"])

                    for item in i_want:
                        print(f"{item['c2cItemsName']},{item['c2cItemsId']},{item['showPrice']}")

                    print(min_element)
                    #自动创建对应搜索物品
                    item_ALL(Srarch_txt.get())
                    # 找到物品弹窗
                    showinfo(title='搜索结果', message='程序运行完毕\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    Srarch_Button.state(['!disabled'])
                    Srarch_txt.state(['!disabled'])
                    Maximum_Price_txt.state(['!disabled'])
                    Minimum_Price_txt.state(['!disabled'])
                    break

                data = response["data"]["data"]
                for item in data:
                    name = item["c2cItemsName"]
                    if str(Srarch_txt.get()) in name:
                        if item not in i_want:
                            i_want.append(item)
                            item_all.append(
                                f"物品名：{item['c2cItemsName']}\n价格：{item['showPrice']}元"
                                f"\n物品链接：https://mall.bilibili.com/neul-next/index.html?page=magic-market_detail&noTitleBar=1&itemsId={item['c2cItemsId']}&from=market_index\n\n")

                #设置输出数量
                if len(item_all) >= int(amount_print_Scale.get()) and int(amount_print_Scale.get()) !=0:
                    # 自动创建对应搜索物品
                    item_ALL(Srarch_txt.get())
                    # 找到物品弹窗
                    showinfo(title='搜索结果',
                            message=f'程序运行完毕\n'
                                    f'已启用输出数量\n'
                                    f'当前目标值为:{amount_print_Scale.get()}\n'
                                    f'请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    Srarch_Button.state(['!disabled'])
                    Srarch_txt.state(['!disabled'])
                    Maximum_Price_txt.state(['!disabled'])
                    Minimum_Price_txt.state(['!disabled'])
                    break

                #间隔时间
                sleep(int(Sleep_Scale.get()))

            except Exception as e:
                print('主搜索程序报错信息:',e)
                sleep(5)

        # 执行搜索线程池
    def search_lock_start():
        if Srarch_txt.get() == '':
            # 未输入物品弹窗
            showinfo(title='error', message='请输入搜索物品')
        elif str(Maximum_Price_txt.get()) == '':
            # 未输入物品弹窗
            showinfo(title='error', message='请输入价格区间\n最大值，最小值都要填!')
        elif str(Minimum_Price_txt.get()) == '':
            # 未输入物品弹窗
            showinfo(title='error', message='请输入价格区间\n最大值，最小值都要填!')
        else:
            # 创建一个新线程
            t = threading.Thread(target=search_lock)
            t.daemon = True
            # 启动线程
            t.start()

    def write_Cookie():
        try:
            file = frozen_dir.app_path() + "/Set/cookie.txt"
            os.startfile(file)
        except Exception as e:
            showinfo(title='错误异常',message=f'{e}')
    def write_URL():
        try:
            file = frozen_dir.app_path() + "/Set/链接地址.txt"
            os.startfile(file)
        except Exception as e:
            showinfo(title='错误异常',message=f'{e}')

    # 搜索区
    Srarch_Label = tk.Label(text='搜索：', foreground='#ffffff', background='#333333')
    Srarch_Label.place(x=30, y=25, width=45, height=50, anchor='nw')
    # 搜索输入框
    Srarch_txt = ttk.Entry()
    Srarch_txt.place(x=90, y=25, width=200, height=50, anchor='nw')
    # 搜索按钮
    Srarch_Button = ttk.Button(text='点击搜索', command=search_lock_start)
    Srarch_Button.place(x=310, y=30, width=100, height=40, anchor='nw')

    #价格区
    Maximum_Price_Label = tk.Label(text='物品最大价格',foreground='#ffffff',background='#333333')
    Maximum_Price_Label.place(x=40,y=100,width=75,height=30,anchor='nw')
    #最大价格输入框
    Maximum_Price_txt = ttk.Entry()
    Maximum_Price_txt.place(x=30,y=140,width=100,height=50,anchor='nw')
    #########
    Minimum_Price_Label =tk.Label(text='物品最小价格',foreground='#ffffff',background='#333333')
    Minimum_Price_Label.place(x=175,y=100,width=75,height=30,anchor='nw')
    #最小价格输入框
    Minimum_Price_txt = ttk.Entry()
    Minimum_Price_txt.place(x=165,y=140,width=100,height=50,anchor='nw')
    ############
    #打折
    discount_Label = tk.Label(text='打折力度',foreground='#ffffff',background='#333333')
    discount_Label.place(x=310,y=100,width=75,height=30,anchor='nw')
    #下拉选择框
    discount_Combobox = ttk.Combobox()
    discount_Combobox.place(x=300,y=140,width=100,height=50,anchor='nw')
    discount_Combobox['value'] = ('默认不选择','3折以下','3-5折','5-7折','7折以上')
    discount_Combobox.current(0)
    ###########
    #排列顺序
    arrangement_Label = tk.Label(text='排序规则',foreground='#ffffff',background='#333333')
    arrangement_Label.place(x=40,y=210,width=75,height=30,anchor='nw')
    #下拉选择框
    arrangement_Combobox = ttk.Combobox()
    arrangement_Combobox.place(x=30,y=250,width=100,height=50,anchor='nw')
    arrangement_Combobox['value'] = ('综合搜索','价格升序搜索','价格降序搜索')
    arrangement_Combobox.current(0)
    #############
    variety_item_Label = tk.Label(text='搜索种类',foreground='#ffffff',background='#333333')
    variety_item_Label.place(x=170,y=210,width=75,height=30,anchor='nw')
    #下拉选择框
    variety_item_Combobox = ttk.Combobox()
    variety_item_Combobox.place(x=160,y=250,width=100,height=50,anchor='nw')
    variety_item_Combobox['value'] = ('手办','模型','周边','3C','福袋')
    variety_item_Combobox.current(0)
    #########
    #cookie设置
    cookie_Button = tk.Button(text='cookie设置',command=write_Cookie)
    cookie_Button.place(x=300,y=255,width=100,height=40)
    #链接设置
    URL_Button = tk.Button(text='链接地址',command=write_URL)
    URL_Button.place(x=300,y=205,width=100,height=40)

    #输出数量
    amount_print_Label = tk.Label(text='搜索多少个\n0为不限制',foreground='#ffffff',background='#333333')
    amount_print_Label.place(x=25,y=310,width=100,height=30,anchor='nw')
    amount_print_Scale = tk.Scale(from_=0, to=20, length=200, resolution=1, orient="horizontal")
    amount_print_Scale.place(x=30, y=355, width=100, height=50, anchor='nw')

    #搜索程序间隔时间
    Sleep_Label = tk.Label(text='搜索间隔时间(秒)',foreground='#ffffff',background='#333333')
    Sleep_Label.place(x=150,y=310,width=120,height=30,anchor='nw')
    Sleep_Scale = tk.Scale(from_=0, to=5, length=200,resolution=0.1,orient="horizontal")
    Sleep_Scale.place(x=160,y=355,width=100,height=50,anchor='nw')
    # 强行终止程序
    Forced_termination_Label = tk.Label(text='手动终止程序',foreground='#ffffff',background='#333333')
    Forced_termination_Label.place(x=290,y=310,width=120,height=30,anchor='nw')
    Forced_termination_Scale = tk.Scale(from_=0, to=5, length=200,resolution=5,orient="horizontal",showvalue=False)
    Forced_termination_Scale.place(x=300,y=375,width=100,height=30,anchor='nw')
    yes_or_no_Label = tk.Label(text='否              是',foreground='#ffffff',background='#333333')
    yes_or_no_Label.place(x=290,y=340,width=120,height=30,anchor='nw')

    #显示请求
    print_Label = tk.Label()
    print_Label.place(x=30,y=425,width=370,height=60)


    # 窗口主程序
    My_Window.mainloop()


item_all = []


def item_ALL(item):
    try:
        # 地址
        file_site = frozen_dir.app_path() + f'/Set/item/{item}.txt'
        # 创建文件
        file_folder(item)
        # 写入
        file = open(file_site, mode='w', encoding='utf-8')
        file.writelines(item_all)
        file.close()
        # 清除
        item_all.clear()
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


#程序主入口
if __name__ == '__main__':
    ALL_Window()
