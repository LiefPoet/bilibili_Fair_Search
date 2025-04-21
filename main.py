import json
import threading
import webbrowser
from tkinter.messagebox import showinfo

import customtkinter
from PIL import Image, ImageTk
import os
import requests
from bs4 import BeautifulSoup
from time import sleep
import gc

import frozen_dir
import Set
import Value_txt


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.item_all_List = []
        # 多线程
        self.start_Event = 'yes'

        self.title("魔力赏搜索")
        ww = 550
        wh = 500
        # self.geometry("400x500")
        self.width = int((self.winfo_screenwidth() - ww) / 2)
        self.height = int((self.winfo_screenheight() - wh) / 2)
        self.geometry(f"{ww}x{wh}+{self.width}+{self.height}")
        self.minsize(550, 500)
        self.maxsize(550, 500)

        try:
            self.iconpath = ImageTk.PhotoImage(file=os.path.join("Set", "f.ico"))
            self.wm_iconbitmap()
            self.iconphoto(False, self.iconpath)
        except:
            pass

        # 搜索栏
        self.Srarch_Entry = customtkinter.CTkEntry(self, width=390, height=40)
        self.Srarch_Entry.grid(row=0, column=0, padx=10, pady=(10, 0), columnspan=3, sticky="ew")

        self.Srarch_Button = customtkinter.CTkButton(self, width=120, height=40, text='点击搜索',
                                                     command=self.search_lock_start)
        self.Srarch_Button.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="nw")

        # 价格选项
        self.Money_Label = customtkinter.CTkLabel(self, width=120, height=20, text='价格选项')
        self.Money_Label.grid(row=1, column=3, padx=10, pady=(10, 0), sticky="nw")
        self.Money_ComboBox = customtkinter.CTkComboBox(self, values=list(Value_txt.Money_Values.keys()), width=120,
                                                        height=40)
        self.Money_ComboBox.grid(row=2, column=3, padx=10, sticky="nw")
        # 打折力度
        self.discount_Label = customtkinter.CTkLabel(self, width=120, height=20, text='打折力度')
        self.discount_Label.grid(row=3, column=3, padx=10, sticky="nw")
        self.discount_ComboBox = customtkinter.CTkComboBox(self, values=list(Value_txt.discount_Values.keys()),
                                                           width=120, height=40)
        self.discount_ComboBox.grid(row=4, column=3, padx=10, sticky="nw")

        # 排序规则
        self.arrangement_Label = customtkinter.CTkLabel(self, width=120, height=20, text='排序规则')
        self.arrangement_Label.grid(row=5, column=3, padx=10, sticky="nw")
        self.arrangement_Combobox = customtkinter.CTkComboBox(self, values=list(Value_txt.arrangement_Values.keys()),
                                                              width=120, height=40)
        self.arrangement_Combobox.grid(row=6, column=3, padx=10, sticky="nw")

        # 搜索种类
        self.variety_item_Label = customtkinter.CTkLabel(self, width=120, height=20, text='搜索种类')
        self.variety_item_Label.grid(row=7, column=3, padx=10, sticky="nw")
        self.variety_item_Combobox = customtkinter.CTkComboBox(self, values=list(Value_txt.variety_item_Values.keys()),
                                                               width=120, height=40)
        self.variety_item_Combobox.grid(row=8, column=3, padx=10, sticky="nw")
        # 搜索个数
        self.amount_print_Label = customtkinter.CTkLabel(self, width=120, height=20, text='搜索限制[0为不限制]')
        self.amount_print_Label.grid(row=9, column=3, padx=10, sticky="nw")
        self.amount_print_Entry = customtkinter.CTkEntry(self, width=120, height=40)
        self.amount_print_Entry.grid(row=10, column=3, padx=10, sticky="nw")
        # 搜索间隔
        self.Sleep_Label = customtkinter.CTkLabel(self, width=120, height=20, text='时间间隔[秒]')
        self.Sleep_Label.grid(row=11, column=3, padx=10, sticky="nw")
        self.Sleep_Entry = customtkinter.CTkEntry(self, width=120, height=40)
        self.Sleep_Entry.grid(row=12, column=3, padx=10, sticky="nw")
        # 链接地址
        self.URL_Button = customtkinter.CTkButton(self, width=120, height=40, text='链接地址', command=Set.write_URL)
        self.URL_Button.grid(row=12, column=0, padx=10, sticky="nw")
        # cookie设置
        self.cookie_Button = customtkinter.CTkButton(self, width=120, height=40, text='cookie设置',
                                                     command=Set.write_Cookie)
        self.cookie_Button.grid(row=12, column=1, padx=5, sticky="nw")
        # 手动终止
        self.Forced_termination_Button = customtkinter.CTkButton(self, width=120, height=40, text='手动终止',
                                                                 command=self.stop_Button)
        self.Forced_termination_Button.grid(row=12, column=2, padx=5, sticky="nw")
        # 锁定手动终止按钮
        self.Forced_termination_Button.configure(state="disabled")

        # 物品列表
        self.itmeList_frame = customtkinter.CTkScrollableFrame(self, width=370, height=300)
        # self.GameList_frame = customtkinter.CTkScrollableFrame(self, width=510, height=300)
        self.itmeList_frame.grid(row=1, column=0, padx=10, pady=10, rowspan=11, columnspan=3, sticky="nw")

        # 输出窗口
        self.print_Label = customtkinter.CTkLabel(self,height=60)
        self.print_Label.grid(row=13, column=0, padx=10, pady=10, columnspan=4, sticky="ew")
        # 重置显示
        self.print_Label.configure(justify="left", anchor="w", text=f'运行代码：\n',
                                   wraplength=520)

        # 物品按钮记录
        self.item_Button = {}

    def stop_Button(self):
        self.start_Event = 'no'
        return self.start_Event

    # 解锁按钮
    def unlock_Button(self):
        # 搜索按钮
        self.Srarch_Button.configure(state="normal")
        # 搜索输入框
        self.Srarch_Entry.configure(state="normal")
        # 价格选项
        self.Money_ComboBox.configure(state="normal")
        # 折扣选项
        self.discount_ComboBox.configure(state="normal")
        # 排序选项
        self.arrangement_Combobox.configure(state="normal")
        # 搜索类别
        self.variety_item_Combobox.configure(state="normal")
        # 搜索个数
        self.amount_print_Entry.configure(state="normal")
        # 搜索间隔
        self.Sleep_Entry.configure(state="normal")

    # 锁定按钮
    def lock_Button(self):
        # 搜索按钮
        self.Srarch_Button.configure(state="disabled")
        # 搜索输入框
        self.Srarch_Entry.configure(state="disabled")
        # 价格选项
        self.Money_ComboBox.configure(state="disabled")
        # 折扣选项
        self.discount_ComboBox.configure(state="disabled")
        # 排序选项
        self.arrangement_Combobox.configure(state="disabled")
        # 搜索类别
        self.variety_item_Combobox.configure(state="disabled")
        # 搜索个数
        self.amount_print_Entry.configure(state="disabled")
        # 搜索间隔
        self.Sleep_Entry.configure(state="disabled")

    # 搜索主逻辑代码
    def search_lock(self):
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
        # ---物品按钮相关---
        num_Button = 0  # 按钮计数
        self.item_Button = {}  # 清空按钮字典
        self.clear_scrollable_frame(self.itmeList_frame)
        # 重置显示
        self.print_Label.configure(justify="left", anchor="w", text=f'运行代码：\n',
                                   wraplength=520)
        # 锁定按钮
        self.lock_Button()
        # 解锁手动终止按钮
        self.Forced_termination_Button.configure(state="normal")

        # 翻页变量
        nextId = None

        # ---获取值---
        # 价格区间
        Money_txt = self.Money_ComboBox.get()
        Money_Value = Value_txt.Money_Values[Money_txt]
        # 打折力度
        Discount_txt = self.discount_ComboBox.get()
        Discount_Value = Value_txt.discount_Values[Discount_txt]
        # 排序规则
        Arrangement_txt = self.arrangement_Combobox.get()
        Arrangement_Value = Value_txt.arrangement_Values[Arrangement_txt]
        # 搜索种类
        Variety_item_txt = self.variety_item_Combobox.get()
        Variety_item_Value = Value_txt.variety_item_Values[Variety_item_txt]

        try:

            while True:
                if self.discount_ComboBox.get() != '默认不选择':
                    payload = json.dumps({
                        "categoryFilter": str(Variety_item_Value),
                        "priceFilters": [
                            str(Money_Value)
                        ],
                        "discountFilters": [
                            str(Discount_Value)
                        ],
                        "nextId": nextId,
                        "sortType": str(Arrangement_Value)
                    })
                else:
                    payload = json.dumps({
                        "categoryFilter": str(Variety_item_Value),
                        "priceFilters": [
                            str(Money_Value)
                        ],
                        "nextId": nextId,
                        "sortType": str(Arrangement_Value)
                    })

                print('储存值：？', payload)
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

                response = requests.request("POST", str(Set.load_URL()), headers=headers, data=payload)
                print_txt = response.text
                self.print_Label.configure(justify="left", anchor="w", text=f'运行代码：\n{print_txt}\n',
                                           wraplength=520)
                response = response.json()
                # 解析网站源码
                soup = BeautifulSoup(print_txt, 'html.parser')
                # 查找是否拥有风控报错信息
                Forced_termination = soup.find('div', class_="error-container")
                # 自动终止程序
                if Forced_termination != None:
                    # 自动创建对应搜索物品
                    self.item_ALL(self.Srarch_Entry.get(), self.item_all_List)
                    # 找到物品弹窗
                    showinfo(title='搜索结果',
                             message='程序已自动终止运行!\n已经风控！\n输出当前全部搜索结果\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    self.unlock_Button()
                    # 锁定手动终止按钮
                    self.Forced_termination_Button.configure(state="disabled")
                    break
                if self.start_Event != 'yes':
                    # 手动停止
                    self.item_ALL(self.Srarch_Entry.get(), self.item_all_List)
                    # 找到物品弹窗
                    showinfo(title='搜索结果',
                             message='程序已手动终止运行!\n输出当前全部搜索结果\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    self.start_Event = 'yes'
                    # 解锁按钮
                    self.unlock_Button()
                    # 锁定手动终止按钮
                    self.Forced_termination_Button.configure(state="disabled")
                    break

                # 拿到翻页的变量
                nextId = response["data"]["nextId"]
                if nextId is None:
                    if i_want == []:
                        # 未找到物品弹窗
                        showinfo(title='搜索结果',
                                 message='未能在规定区间找到所选物品\n请扩大搜索区间或检查搜索名称')
                        # 解锁按钮
                        self.unlock_Button()
                        # 锁定手动终止按钮
                        self.Forced_termination_Button.configure(state="disabled")
                        break

                    print("+++++++++++++++++++++")
                    print(i_want)
                    print("=========================")
                    min_element = min(i_want, key=lambda x: x["showPrice"])

                    for item in i_want:
                        print(f"{item['c2cItemsName']},{item['c2cItemsId']},{item['showPrice']}")

                    print(min_element)
                    # 自动创建对应搜索物品
                    self.item_ALL(self.Srarch_Entry.get(), self.item_all_List)
                    # 找到物品弹窗
                    showinfo(title='搜索结果', message='程序运行完毕\n请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    self.unlock_Button()
                    # 锁定手动终止按钮
                    self.Forced_termination_Button.configure(state="disabled")
                    break

                data = response["data"]["data"]
                for item in data:
                    name = item["c2cItemsName"]
                    if str(self.Srarch_Entry.get()) in name:
                        if item not in i_want:
                            item_Img = item['detailDtoList'][0]['img']
                            num_Button += 1
                            itme_Img_Url = "https:"+item_Img
                            print('按钮计数？：', num_Button)
                            #print('图片地址？', item_Img[2:])
                            print('图片地址？', itme_Img_Url)
                            # 加入字典
                            self.item_Button.setdefault(item['c2cItemsId'],item['c2cItemsName'])
                            print('物品按钮信息',self.item_Button)
                            # 物品对应图片
                            item_image = customtkinter.CTkImage(
                                light_image=Image.open(
                                    requests.get(itme_Img_Url, headers=headers, stream=True).raw),
                                size=(50, 50))
                            # 创建物品对应按钮
                            itemName_Button = f"https://mall.bilibili.com/neul-next/index.html?page=magic-market_detail&noTitleBar=1&itemsId={item['c2cItemsId']}&from=market_index"
                            print('是否单个参数：',itemName_Button)
                            self.item_Button[item['c2cItemsId']] = customtkinter.CTkButton(self.itmeList_frame, image=item_image,
                                                                             text=f"{item['showPrice']}元 ———{item['c2cItemsName']}",
                                                                             width=500, anchor='nw',
                                                                             command=lambda itemName_1=str(itemName_Button)
                                                                             : threading.Thread(
                                                                                 target=self.items_url_Button,
                                                                                 args=(itemName_1,),
                                                                                 daemon=True).start())
                            self.item_Button[item['c2cItemsId']].grid(row=num_Button, column=0, padx=10, pady=(10, 0), sticky="sw")
                            i_want.append(item)
                            self.item_all_List.append(
                                f"物品名：{item['c2cItemsName']}\n价格：{item['showPrice']}元"
                                f"\n物品链接：https://mall.bilibili.com/neul-next/index.html?page=magic-market_detail&noTitleBar=1&itemsId={item['c2cItemsId']}&from=market_index\n\n")

                # 设置输出数量
                if len(self.item_all_List) >= int(self.amount_print_Entry.get()) and int(self.amount_print_Entry.get()) != 0:
                    # 自动创建对应搜索物品
                    self.item_ALL(self.Srarch_Entry.get(), self.item_all_List)
                    # 找到物品弹窗
                    showinfo(title='搜索结果',
                    message = f'程序运行完毕\n'
                    f'已启用输出数量\n'
                    f'当前目标值为:{self.amount_print_Entry.get()}\n'
                    f'请去根目录Set文件夹中item文件夹查看搜索结果')
                    # 解锁按钮
                    self.unlock_Button()
                    # 锁定手动终止按钮
                    self.Forced_termination_Button.configure(state="disabled")

                    break


                # 间隔时间
                sleep(int(self.Sleep_Entry.get()))


        except Exception as e:
            print('主搜索程序报错信息:', e)
            sleep(5)


    def search_lock_start(self):
        # 创建一个新线程
        t = threading.Thread(target=self.search_lock)
        t.daemon = True
        # 启动线程
        t.start()


    def item_ALL(self, item, itme_list):
        try:
            # 地址
            file_site = frozen_dir.app_path() + f'/Set/item/{item}.txt'
            # 创建文件
            Set.file_folder(item)
            # 写入
            file = open(file_site, mode='w', encoding='utf-8')
            file.writelines(itme_list)
            file.close()
            # 清除
            itme_list.clear()
        except Exception as e:
            showinfo(title='错误异常', message=f'{e}')

    # 打开网页
    def items_url_Button(self, url):
        item_url = url
        webbrowser.open(item_url)
    # 清空物品按钮
    def clear_scrollable_frame(self,frame):
        """ 清空滚动框架内所有子组件 """
        # 遍历并销毁所有子组件
        for widget in frame.winfo_children():
            widget.destroy()

        # 可选：重置布局记忆（针对复杂布局）
        frame.grid_rowconfigure(0, weight=0)  # 重置行权重
        frame._parent_canvas.yview_moveto(0)  # 滚动条复位到顶部
        # 强制垃圾回收
        gc.collect()


'''
        # 进度条
self.Srarch_ProgressBar = customtkinter.CTkProgressBar(self, width=20, height=10)
self.Srarch_ProgressBar.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")
self.Srarch_ProgressBar.set(0)
# 保存位置显示
self.download_path_Text = customtkinter.CTkLabel(self, width=390, height=20, font=('Segoe UI', 15),
                                                 wraplength=390, justify='left')
self.download_path_Text.grid(row=3, column=0, padx=10, pady=10, sticky="nw")

self.download_path_Button = customtkinter.CTkButton(self, text="更改保存位置", width=120, height=40,
                                                    command=self.download_path_txt)
self.download_path_Button.grid(row=3, column=1, padx=10, pady=10, sticky="nw")
# 记录按钮
self.item_Button = {}
'''

if __name__ == "__main__":
    app = App()
    app.mainloop()
