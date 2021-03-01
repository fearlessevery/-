# -*- coding:utf-8 -*-
from ListGet import *
from RankingGet import hot_search
from DownloadGet import getDownloadUrl
from ClipboardOP import setClip
from OnlineGet import getOnlineUrl
from InitConfig import PATHConfig
pathConfig=PATHConfig()
# from RankingView import *

from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import Tk
from tkinter import ttk
from tkinter import font
from tkinter import LabelFrame
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import END
from tkinter import Button
from tkinter import Frame
from tkinter import RIGHT,BOTTOM
from tkinter import NSEW
from tkinter import NS
from tkinter import NW
from tkinter import N
from tkinter import Y,X
from tkinter import DISABLED
from tkinter import NORMAL
from threading import Thread
from webbrowser import open
# import os
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context #关闭SSL证书验证


"""重新定义带返回值的线程类"""
class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args


    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
def thread_it(func, *args):
    # 创建
    t = Thread(target=func, args=args)
    # 守护
    t.setDaemon(True)
    # 启动
    t.start()
    # print('end')

def handlerAdaptor(fun, **kwds):
    '''事件处理函数的适配器，相当于中介，那个event是从那里来的呢，我也纳闷，这也许就是python的伟大之处吧'''
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

def resize(w_box, h_box, pil_image):
    """
    等比例缩放图片,并且限制在指定方框内
    :param w_box,h_box: 指定方框的宽度和高度
    :param pil_image: 原始图片
    :return:
    """
    f1 = 1.0 * w_box / pil_image.size[0]  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / pil_image.size[1]
    factor = min([f1, f2])
    # print(f1, f2, factor) # test
    # use best down-sizing filter
    width = int(pil_image.size[0] * factor)
    height = int(pil_image.size[1] * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)


class uiObject:

    def __init__(self):
        self.doubanUrl=""

    def open_ranking(self):
        # print(self.ranking_type.get())
        self.clear_tree(self.treeview_ranking)
        self.label_bar['state'] = DISABLED
        self.label_reli['state'] = DISABLED
        self.add_tree([['正在更新...', '', '']], self.treeview_ranking)
        lst=hot_search(self.ranking_type.get())
        self.clear_tree(self.treeview_ranking)
        self.add_tree(lst, self.treeview_ranking)  # 将数据添加到tree中
        self.label_bar['state'] = NORMAL
        self.label_reli['state'] = NORMAL
    def open_Online(self):
        self.clear_tree(self.treeview_play_online)
        self.add_tree([['正在努力搜索...', '', '']], self.treeview_play_online)
        resultOnline = getOnlineUrl(self.T_vote_keyword.get())
        self.clear_tree(self.treeview_play_online)
        self.add_tree(resultOnline, self.treeview_play_online)

    def open_Download(self):
        # print(self.ranking_type.get())
        self.clear_tree(self.treeview_bt_download)
        self.add_tree([['正在努力搜索...','','']], self.treeview_bt_download)
        resultDownload=getDownloadUrl(self.T_vote_keyword.get())
        self.clear_tree(self.treeview_bt_download)
        self.add_tree(resultDownload, self.treeview_bt_download)
    def open_ranking_event(self, event):
        thread_it(func=self.open_ranking)
    def show_detail_img(self, file_name):
        img_open = Image.open(file_name) #读取本地图片
        pil_image_resized = resize(160, 230, img_open) #等比例缩放本地图片
        img = ImageTk.PhotoImage(pil_image_resized) #读入图片
        self.label_img.config(image=img, width = pil_image_resized.size[0], height = pil_image_resized.size[1])
        self.label_img.image = img
    def openLocalHtml(self,event,url):
        if self.label_bar['state'] == NORMAL:
            newurl=pathConfig.HTLMSPATH + self.ranking_type.get()+url
            open(newurl)

    def center_window(self, root, w, h):
        """
        窗口居于屏幕中央
        :param root: root
        :param w: 窗口宽度
        :param h: 窗口高度
        :return:
        """
        # 获取屏幕 宽、高
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()

        # 计算 x, y 位置
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))



    def clear_tree(self, tree):
        '''
        清空表格
        '''
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def add_tree(self,list, tree):
        '''
        新增数据到表格
        '''
        i = 0
        for subList in list:
            tree.insert('', 'end', values=subList)
            i = i + 1
        tree.grid()
    def keyboard_T_vote_keyword(self, event):
        thread_it(self.searh_movie_in_keyword)


    #def refresh_Online(self):
    def thread_view(self,fname,tree, args):
        # 创建
        t = MyThread(func=fname, args=args)
        # 守护
        t.setDaemon(True)
        # 启动
        t.start()
        t.join()
        result = t.get_result()
        self.add_tree(result,tree)

        # print(result)
        # self.add_tree(result,tree)
    def searh_movie_in_keyword(self):#从关键字中搜索符合条件的影片信息
        if self.T_vote_keyword.get()!='':
            # 按钮设置为灰色状态
            self.clear_tree(self.treeview)  # 清空表格
            # self.clear_tree(self.treeview_bt_download)
            # self.clear_tree(self.treeview_play_online)

            self.B_0_keyword['state'] = DISABLED
            self.T_vote_keyword['state'] = DISABLED#s搜索的文本
            self.B_0_keyword['text'] = '正在努力搜索'
            thread_it(func=self.open_Online)
            thread_it(func=self.open_Download)
            self.add_tree([['正在努力搜索...', '', '']], self.treeview)
            # self.thread_view(fname=getList, tree=self.treeview, args=(self.T_vote_keyword.get(),))
            # self.thread_view(fname=getOnlineUrl, tree=self.treeview_play_online, args=(self.T_vote_keyword.get(),))
            # self.thread_view(fname=getDownloadUrl, tree=self.treeview_bt_download, args=(self.T_vote_keyword.get(),))

            result=getList(self.T_vote_keyword.get())
            self.clear_tree(self.treeview)  # 清空表格
            self.add_tree(result,self.treeview) # 将数据添加到tree中



            # resultOnline = getOnlineUrl(self.T_vote_keyword.get())
            # self.add_tree(resultOnline, self.treeview_play_online)
            #
            # resultDownload=getDownloadUrl(self.T_vote_keyword.get())
            # self.add_tree(resultDownload, self.treeview_bt_download)

            # 按钮设置为正常状态
            self.B_0_keyword['state'] = NORMAL
            self.T_vote_keyword['state'] = NORMAL
            self.B_0_keyword['text'] = '搜索'
        else:
            messagebox.showerror('什么都没有输入ｂ（￣▽￣）ｄ', '输入后再来搜索吧(^_−)☆')
    def open_details(self):
        item = self.treeview.selection()
        if len(item)>0:
            detail_url=self.treeview.item(item, "values")[-1]
            # self.label_details['text'] = '加载中......'
            self.douban['text']='加载中......'
            self.label_details['text']=getDetails(detail_url)
            self.show_detail_img(pathConfig.IMAGESPATH+'details.png')
            self.doubanUrl=detail_url
            self.douban['text'] = '去豆瓣查看'
    def open_details_event(self,event):
        thread_it(func=self.open_details)

    def copyURL(self,event):
        item = self.treeview_bt_download.selection()
        if (item):
            item_text = self.treeview_bt_download.item(item, "values")
            url = item_text[3]
            setClip(url)
            messagebox.showinfo('复制链接成功', '链接：'+url)

    def open_in_browser(self, event):
        item = self.treeview_bt_download.selection()
        # print('hello')
        # print(item)
        if(item):
            item_text = self.treeview_bt_download.item(item, "values")
            url = item_text[4]
            open(url)
    def open_in_browser_online(self,event):
        item = self.treeview_play_online.selection()
        # print('hello')
        # print(item)
        if (item):
            item_text = self.treeview_play_online.item(item, "values")
            url = item_text[2]
            open(url)
    def ui_process(self):
        root = Tk()
        root.iconbitmap('logo.ico')

        self.root = root
        # 设置窗口位置
        root.title("影视助手")
        self.center_window(root, 1200, 565)
        root.resizable(0, 0)  # 框体大小可调性，分别表示x,y方向的可变性Ranking
#################################################################################################排行榜
        ranking_frame = LabelFrame(root, width=200, height=300, text="排行榜")
        ranking_frame.place(x=5, y=5)
        label_select=Label(ranking_frame, text='请选择')
        label_select.place(x=5, y=5)

        comvalue = StringVar()
        ranking_type = ttk.Combobox(ranking_frame, width=5, textvariable=comvalue, state='readonly')
        movieList = ['电视剧','电影']
        ranking_type["values"] = movieList  # 初始化
        ranking_type.current(0)  # 选择第一个
        ranking_type.place(x=45, y=5)
        self.ranking_type = ranking_type

        # label_bar = Label(ranking_frame, text='条形图')
        # label_bar.place(x=110, y=5)

        self.label_bar = Label(ranking_frame, text="条形图", fg="blue", cursor="hand2")
        self.label_bar.place(x=110, y=10)
        # self.label_bar.bind("<Button-1>", lambda event: open(r'E:/python projects/project_an/htmls/'+self.ranking_type.get()+r'Bar图.html'))
        self.label_bar.bind("<Button-1>",handlerAdaptor(fun=self.openLocalHtml,
                                                        url='Bar图.html'))
        self.label_reli = Label(ranking_frame, text="热力图", fg="blue", cursor="hand2")
        self.label_reli.place(x=150, y=10)
        # self.label_reli.bind("<Button-1>", lambda event: open(HTLMSPATH+self.ranking_type.get()+r'热力图.html'))
        self.label_reli.bind("<Button-1>", handlerAdaptor(fun=self.openLocalHtml,
                                                         url='热力图.html'))



        frame_root_ranking = Frame(ranking_frame)

        frame_l_ranking = Frame(frame_root_ranking)
        frame_r_ranking = Frame(frame_root_ranking)
        self.ranking_frame = ranking_frame
        self.frame_l_ranking = frame_l_ranking
        self.frame_r_ranking = frame_r_ranking

        columns = ("名字", "热度")
        treeview_ranking = ttk.Treeview(frame_l_ranking, height=10, show="headings", columns=columns)

        treeview_ranking.column("名字", width=100, anchor='center')  # 表示列,不显示
        treeview_ranking.column("热度", width=60, anchor='center')


        treeview_ranking.heading("名字", text="名字")  # 显示表头
        treeview_ranking.heading("热度", text="热度")

        # 垂直滚动条
        vbar_ranking = ttk.Scrollbar(frame_r_ranking, command=treeview_ranking.yview)
        treeview_ranking.configure(yscrollcommand=vbar_ranking.set)
        treeview_ranking.pack()
        self.treeview_ranking = treeview_ranking
        vbar_ranking.pack(side=RIGHT, fill=Y)
        self.vbar_ranking = vbar_ranking
        # 框架的位置布局
        frame_l_ranking.grid(row=0, column=0, sticky=NSEW)
        frame_r_ranking.grid(row=0, column=1, sticky=NS)
        frame_root_ranking.place(x=5, y=45)

#################################################################################################搜索电影
        # 容器控件
        labelframe = LabelFrame(root, width=650, height=300, text="搜索电影(点击搜索结果查看详情)")
        labelframe.place(x=215, y=5)
        self.labelframe = labelframe
        # 电影搜索
        # 影片名称
        L_vote_keyword = Label(labelframe, text='影片名称')
        L_vote_keyword.place(x=0, y=10)
        #L_vote_keyword.grid(row=0,column=0)
        self.L_vote_keyword = L_vote_keyword
        # 文本框
        T_vote_keyword = Entry(labelframe, width=53)
        T_vote_keyword.delete(0, END)
        T_vote_keyword.insert(0, '')
        T_vote_keyword.place(x=66, y=7)
        self.T_vote_keyword = T_vote_keyword
        # 查询按钮
        #lambda表示绑定的函数需要带参数，请勿删除lambda，否则会出现异常
        #thread_it表示新开启一个线程执行这个函数，防止GUI界面假死无响应
        B_0_keyword = Button(labelframe, text="搜索")
        B_0_keyword.place(x=460, y=7)

        frame_root = Frame(labelframe, width=400)
        frame_l = Frame(frame_root)
        frame_r = Frame(frame_root)
        self.frame_root = frame_root
        self.frame_l = frame_l
        self.frame_r = frame_r

        self.B_0_keyword = B_0_keyword
        columns = ("名字", "评分", "相关")
        treeview = ttk.Treeview(frame_l, height=10, show="headings", columns=columns)

        treeview.column("名字", width=120, anchor='center')  # 表示列,不显示
        treeview.column("评分", width=120, anchor='center')
        treeview.column("相关", width=280, anchor='center')

        treeview.heading("名字", text="名字")  # 显示表头
        treeview.heading("评分", text="评分")
        treeview.heading("相关", text="相关")

        # 垂直滚动条
        vbar = ttk.Scrollbar(frame_r, command=treeview.yview)
        treeview.configure(yscrollcommand=vbar.set)
        # rbar = ttk.Scrollbar(frame_r, command=treeview.xview)
        # treeview.configure(xscrollcommand=rbar.set)

        treeview.pack()
        self.treeview = treeview
        vbar.pack(side=RIGHT, fill=Y)
        self.vbar = vbar
        # rbar.pack(side= BOTTOM, fill=X)
        # self.rbar = rbar

        # 框架的位置布局
        frame_l.grid(row=0, column=0, sticky=NSEW)
        frame_r.grid(row=0, column=1, sticky=NS)
        frame_root.place(x=5, y=45)

#################################################################################################详情
        labelframe_movie_detail = LabelFrame(root, text="影片详情")
        labelframe_movie_detail.place(x=770, y=5)
        self.labelframe_movie_detail = labelframe_movie_detail
        # 框架布局，承载多个控件
        frame_left_movie_detail = Frame(labelframe_movie_detail, width=160,height=380)
        frame_left_movie_detail.grid(row=0, column=0)
        self.frame_left_movie_detail = frame_left_movie_detail
        frame_right_movie_detail = Frame(labelframe_movie_detail, width=260,height=380)
        frame_right_movie_detail.grid(row=0, column=1)
        self.frame_right_movie_detail = frame_right_movie_detail
        #影片图片
        self.label_img = Label(frame_left_movie_detail, text="", anchor=N)
        self.label_img.place(x=0,y=0) #布局
        self.label_img = self.label_img

        self.douban = Label(frame_left_movie_detail, text="", fg="blue", cursor="hand2")
        self.douban.place(x=0, y=210)
        self.douban.bind("<Button-1>", lambda event: open(self.doubanUrl))

        ft = font.Font(size=8, weight=font.BOLD)
        label_details = Label(frame_right_movie_detail, text='',justify='left',anchor=NW,wraplength=250)
        label_details.place(x=10, y=10)
        # label_details.pack()
        self.label_details = label_details

#################################################################################################在线播放
        labelframe_movie_play_online = LabelFrame(root, width=310, height=235, text="在线观看(双击播放)")
        labelframe_movie_play_online.place(x=5, y=305)
        self.labelframe_movie_play_online = labelframe_movie_play_online

        # 框架布局，承载多个控件
        frame_root_play_online = Frame(labelframe_movie_play_online, width=324)
        frame_l_play_online = Frame(frame_root_play_online)
        frame_r_play_online = Frame(frame_root_play_online)
        self.frame_root_play_online = frame_root_play_online
        self.frame_l_play_online = frame_l_play_online
        self.frame_r_play_online = frame_r_play_online
        # 表格
        columns_play_online = ("名称", "来源","播放地址")
        treeview_play_online = ttk.Treeview(frame_l_play_online, height=9, show="headings", columns=columns_play_online)
        treeview_play_online.column("名称", width=110, anchor='center')
        treeview_play_online.column("来源", width=50, anchor='center')
        treeview_play_online.column("播放地址", width=120, anchor='center')
        treeview_play_online.heading("名称", text="名称")
        treeview_play_online.heading("来源", text="来源")
        treeview_play_online.heading("播放地址", text="播放地址")

        #垂直滚动条
        vbar_play_online = ttk.Scrollbar(frame_r_play_online, command=treeview_play_online.yview)
        treeview_play_online.configure(yscrollcommand=vbar_play_online.set)

        treeview_play_online.pack()
        self.treeview_play_online = treeview_play_online
        vbar_play_online.pack(side=RIGHT, fill=Y)
        self.vbar_play_online = vbar_play_online

        # 框架的位置布局
        frame_l_play_online.grid(row=0, column=0, sticky=NSEW)
        frame_r_play_online.grid(row=0, column=1, sticky=NS)
        frame_root_play_online.place(x=5, y=0)

#################################################################################################下载
        labelframe_movie_bt_download = LabelFrame(root, width=440, height=235, text="影视下载(选中条目右击复制下载地址，双击进入网页介绍)")
        labelframe_movie_bt_download.place(x=320, y=305)
        self.labelframe_movie_bt_download = labelframe_movie_bt_download

        # 框架布局，承载多个控件
        frame_root_bt_download = Frame(labelframe_movie_bt_download, width=324)
        frame_l_bt_download = Frame(frame_root_bt_download)
        frame_r_bt_download = Frame(frame_root_bt_download)
        self.frame_root_bt_download = frame_root_bt_download
        self.frame_l_bt_download = frame_l_bt_download
        self.frame_r_bt_download = frame_r_bt_download

        # 表格
        columns_bt_download = ("标题", "来源","地址")
        treeview_bt_download = ttk.Treeview(frame_l_bt_download, height=9, show="headings", columns=columns_bt_download)
        treeview_bt_download.column("标题", width=110, anchor='center')
        treeview_bt_download.column("来源", width=100, anchor='center')
        treeview_bt_download.column("地址", width=200, anchor='center')
        treeview_bt_download.heading("标题", text="标题")
        treeview_bt_download.heading("来源", text="来源")
        treeview_bt_download.heading("地址", text="地址")

        #垂直滚动条
        vbar_bt_download = ttk.Scrollbar(frame_r_bt_download, command=treeview_bt_download.yview)
        treeview_bt_download.configure(yscrollcommand=vbar_bt_download.set)

        treeview_bt_download.pack()
        self.treeview_bt_download = treeview_bt_download
        vbar_bt_download.pack(side=RIGHT, fill=Y)
        self.vbar_bt_download = vbar_bt_download

        # 框架的位置布局
        frame_l_bt_download.grid(row=0, column=0, sticky=NSEW)
        frame_r_bt_download.grid(row=0, column=1, sticky=NS)
        frame_root_bt_download.place(x=5, y=0)

#################################################################################################云盘
        labelframe_movie_save_cloud_disk = LabelFrame(root, width=420, height=135, text="云盘搜索")
        labelframe_movie_save_cloud_disk.place(x=770, y=405)
        self.labelframe_movie_save_cloud_disk = labelframe_movie_save_cloud_disk
        # 框架布局，承载多个控件
        frame_root_save_cloud_disk = Frame(labelframe_movie_save_cloud_disk, width=420)
        frame_l_save_cloud_disk = Frame(frame_root_save_cloud_disk)
        frame_r_save_cloud_disk = Frame(frame_root_save_cloud_disk)
        self.frame_root_save_cloud_disk = frame_root_save_cloud_disk
        self.frame_l_save_cloud_disk = frame_l_save_cloud_disk
        self.frame_r_save_cloud_disk = frame_r_save_cloud_disk
        # 表格
        columns_save_cloud_disk = ("来源名称", "是否有效", "播放地址")
        treeview_save_cloud_disk = ttk.Treeview(frame_l_save_cloud_disk, height=4, show="headings",columns=columns_save_cloud_disk)
        treeview_save_cloud_disk.column("来源名称", width=120, anchor='center')
        treeview_save_cloud_disk.column("是否有效", width=110, anchor='center')
        treeview_save_cloud_disk.column("播放地址", width=150, anchor='center')
        treeview_save_cloud_disk.heading("来源名称", text="来源名称")
        treeview_save_cloud_disk.heading("是否有效", text="是否有效")
        treeview_save_cloud_disk.heading("播放地址", text="播放地址")
        # 垂直滚动条
        vbar_save_cloud_disk = ttk.Scrollbar(frame_r_save_cloud_disk, command=treeview_save_cloud_disk.yview)
        treeview_save_cloud_disk.configure(yscrollcommand=vbar_save_cloud_disk.set)
        treeview_save_cloud_disk.pack()
        self.treeview_save_cloud_disk = treeview_save_cloud_disk
        vbar_save_cloud_disk.pack(side=RIGHT, fill=Y)
        self.vbar_save_cloud_disk = vbar_save_cloud_disk
        # 框架的位置布局
        frame_l_save_cloud_disk.grid(row=0, column=0, sticky=NSEW)
        frame_r_save_cloud_disk.grid(row=0, column=1, sticky=NS)
        frame_root_save_cloud_disk.place(x=5, y=0)
        # 保存到云盘布局结束


        #绑定事件
        treeview.bind('<ButtonRelease-1>',self.open_details_event)#搜索结果单击绑定详情

        treeview_bt_download.bind('<ButtonRelease-3>', self.copyURL)#下载列表绑定选中右击复制和双击打开网页
        treeview_bt_download.bind('<Double-1>', self.open_in_browser)

        treeview_play_online.bind('<Double-1>', self.open_in_browser_online)#在线播放绑定左键双击播放
        # treeview_save_cloud_disk.bind('<Double-1>', self.open_in_browser_cloud_disk)  # 表格绑定左键双击事件
        ranking_type.bind('<<ComboboxSelected>>',self.open_ranking_event)#排行榜combox绑定修改事件
        B_0_keyword.configure(command=lambda:thread_it(self.searh_movie_in_keyword)) #按钮绑定单击事件
        T_vote_keyword.bind('<Return>', handlerAdaptor(self.keyboard_T_vote_keyword))  # 文本框绑定回车
        # label_bar.bind('<Double-1>',open(r'E:\python projects\project_an\htmls\电影Bar图.html'))
        # self.open_ranking()#初始化排行榜
        thread_it(self.open_ranking)
        root.mainloop()
ui = uiObject()
ui.ui_process()