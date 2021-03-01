from pyecharts import Bar
from pyecharts import HeatMap
import random
from pyecharts import WordCloud
from pyecharts import Bar3D
import random
from InitConfig import PATHConfig
pathConfig=PATHConfig()
def dainying_bang(x):
    pian,performance=[],[]
    for i in x:
        pian.append(i[0])
        Str =''.join(i[1].split(','))
        performance.append(int(Str))
    # print(pian,performance)
    bar = Bar("这是电影的热度指数", "名字无法全部显示")
    bar.add("电影",pian, performance)
    # bar.show_config()
    bar.render(pathConfig.HTLMSREPATH+'电影Bar图.html')
def dainshi_bang(x):
    pian,performance=[],[]
    for i in x:
        pian.append(i[0])
        Str =''.join(i[1].split(','))#注意这里i[2]是一个对象
        performance.append(int(Str))
    # print(pian,performance)
    bar = Bar("这是电视剧的热度指数", "名字无法全部显示")
    bar.add("电视剧",pian, performance)
    # bar.show_config()
    bar.render(pathConfig.HTLMSREPATH+'电视剧Bar图.html')
    bar.width=1500


def reli(t):
    x_axis, y_axis, y = [], [], []
    for i in t:
        x_axis.append(i[0])
        Str = ''.join(i[1].split(','))  # 注意这里i[2]是一个对象
        y.append(int(int(Str)/200))
    # print(x_axis, y)
    y_axis = [
        "one", "two", "three", "four", "five", "six"]

    da, data = [], []
    for i in y:
        # 生成7个随机数，是他们的和为i
        while 1:
            n1 = random.randint(0, i)
            n2 = random.randint(0, i)
            n3 = random.randint(0, i)
            n4 = random.randint(0, i)
            n5 = random.randint(0, i)
            n6 = random.randint(0, i)
            su = n1 + n2 + n3 + n4 + n5 + n6
            if su == i:
                listRandom = n1, n2, n3, n4, n5, n6
                break
        da.append(listRandom)
    for i in range(50):
        for j in range(6):
            x = [i, j, da[i][j]]
            data.append(x)

    # print(data)
    heatmap = HeatMap()
    heatmap.add(
        "电影热力图",
        x_axis,
        y_axis,
        data,
        is_visualmap=True,
        visual_text_color="#000",
        visual_orient="horizontal",
    )
    heatmap.render(pathConfig.HTLMSREPATH+'电影热力图.html')




def reli2(t):
    bar3d = Bar3D("3D 柱状图示-热播电视剧", width=1200, height=600)
    x_axis, y_axis, y = [], [], []
    for i in t:
        x_axis.append(i[0])
        Str = ''.join(i[1].split(','))  # 注意这里i[2]是一个对象
        y.append(int(int(Str) / 1500))
    x_axis = x_axis
    # print(x_axis, y)
    y_axis = ["one", "two", "three", "four", "five", "six"]

    da, data = [], []
    for i in y:
        # 生成7个随机数，是他们的和为i
        while 1:
            n1 = random.randint(0, i)
            n2 = random.randint(0, i)
            n3 = random.randint(0, i)
            n4 = random.randint(0, i)
            n5 = random.randint(0, i)
            n6 = random.randint(0, i)
            su = n1 + n2 + n3 + n4 + n5 + n6
            if su == i:
                listRandom = n1, n2, n3, n4, n5, n6
                break
        da.append(listRandom)
    for i in range(6):
        for j in range(50):
            x = [i, j, da[j][i]]
            data.append(x)

    # print(data)
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf']
    bar3d.add(
        "",
        x_axis,
        y_axis,
        [[d[1], d[0], d[2]] for d in data],
        is_visualmap=True,
        visual_range=[0, 80],
        visual_range_color=range_color,
        grid3d_width=200,
        grid3d_depth=80,
        grid3d_shading="lambert",
        is_grid3d_rotate=True,
        #         grid3d_rotate_speed=180
    )
    bar3d.render(pathConfig.HTLMSREPATH+'电视剧热力图.html')


def word_cloud(t):
    name,value=[],[]
    x,y=t[0],t[1]
    for i in range(15):
        # print(x[i][1],y[i][1])
        name.append(x[i][0])
        name.append(y[i][0])
        Str =''.join(x[i][1].split(','))#注意这里i[2]是一个对象
        value.append(int(Str))
        Str =''.join(y[i][1].split(','))#注意这里i[2]是一个对象
        value.append(int(Str))
    wordcloud =WordCloud(width=1300, height=620)
    wordcloud.add("", name, value, word_size_range=[20, 100])
    # wordcloud.show_config()
    wordcloud.render(pathConfig.HTLMSREPATH+'词云.html')
