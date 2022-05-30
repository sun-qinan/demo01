from pyecharts import options as opts
from pyecharts.charts import Page, WordCloud, Scatter
from pyecharts.charts import Bar, Page, Grid
import jieba
import pymysql
from pyecharts.charts import Pie
from pyecharts.charts import Line


def dq_mysql(b_name):
    try:
        db = pymysql.connect(host='localhost', user='root', password='', database='text', charset='utf8')
        print('数据库连接成功')
        cur = db.cursor()
        # 查询表中数据
        sql = f"select * from {b_name}"
        cur.execute(sql)
        results = cur.fetchall()

        return results
    except pymysql.Error as e:
        print('数据库查询失败' + str(e))
    db.close()


bg_sj = dq_mysql('sj_shouji')
bbb = ['华为', '金立', '魅族', '荣耀', '努比亚', '一加', '小米', 'vivo', 'OPPO', 'ZTE中兴', '联想', '锤子', '360手机', '魅蓝', 'ivvi', 'TCL',
       '小辣椒', '酷派', '酷比', '乐视', '海信', 'imoo', 'Gigaset', '长虹', '康佳', '美图', '邦华', '蓝魔', 'ZUK', '中国移动', '守护宝', 'iuni',
       'THL', '青橙', '百分之百', '神舟', '卓普', '百事', '大可乐', '天语', '龙酷', '纽曼', '影驰', '云狐', '爱国者', '北斗', '经纬', '盛大', '优派', '海尔',
       'HKC', '夏新', '英华达', '万利达', '基伍', 'HIKe', '波导', '朵唯', '果冻', '泰丰', '欧恩', '多普达', '读者', '首派', '中恒', '摩西', '139易',
       'nibiru', '宇达电通MIO', '锋达通', '英华通', 'i-mate', '齐乐', '七喜', '优米', '凡尔纳', '创维', 'E人E本', '小蜜蜂', '小宇宙', '格力', '佳域',
       'SUGAR', '8848', '博迪', '国虹', '路虎', '奥克斯', '尼凯恩', 'PPTV', '苹果', '摩托罗拉', '诺基亚', '黑莓', '飞利浦', '富可视', '微软', '亚马逊',
       '谷歌', '戴尔', '惠普', 'Palm', '阿尔卡特', '迪士尼', '三星', '夏普', '索尼', 'LG', '索尼爱立信', '现代', 'NEC', '富士通', '东芝', '京瓷', '卡西欧',
       '泛泰', '美晨', '华硕', 'HTC', '宏碁', '技嘉', '华晶']
strs = ''
for i in bg_sj:
    strs = strs + i[0]


def trans_CN(text):
    word_list = jieba.cut(text)
    result = " ".join(word_list)
    return result


d1 = {}
text = trans_CN(strs)
for t in bbb:
    ts = 0
    for i in text.split(' '):
        if t in i:
            ts = ts + 1
    d1[t] = ts
words = []
for i in d1:
    if d1[i] > 0:
        words.append((i, d1[i]))


def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
            .add("", words, word_size_range=[20, 150])
            .set_global_opts(title_opts=opts.TitleOpts(title="手机品牌词云"))
    )
    return c


wd = wordcloud_base()

di4 = {}
c4 = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            di4[t] = di4.get(t, 0) + 1
for i in di4:
    c4.append([i, di4[i]])


def px(f):
    return f[1]


c4.sort(key=px, reverse=True)
cate = []
data = []
age = 0
for i in c4[:10]:
    cate.append(i[0])
    data.append(i[1])
    age = age + i[1]
cate.append('其他')
data.append(len(bg_sj) - age)
pie = Pie()
pie.add("", [list(z) for z in zip(cate, data)]
        , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
pie.set_global_opts(
    title_opts=opts.TitleOpts(title="手机品牌饼图", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
w1 = []
for i in bg_sj:
    ''.replace('商品毛重：', '').replace('kg', '000').replace('g', '')
    zl = i[2].replace('商品毛重：', '').replace('g', '')
    if 'k' in zl:
        zl = float(zl.replace('k', '')) * 1000
    else:
        zl = float(zl)
    w1.append(zl)
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            zl = i[2].replace('商品毛重：', '').replace('g', '')
            if 'k' in zl:
                zl = float(zl.replace('k', '')) * 1000
            else:
                zl = float(zl)
            if zl < 1100:
                d[t] = d.get(t, 0) + zl
                e[t] = e.get(t, 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])


def px(f):
    return f[1]


c.sort(key=px, reverse=True)
x = []
y = []
for i in c[2:12]:
    x.append(i[0])
    y.append(i[1])
# bar = Bar(init_opts=opts.InitOpts(bg_color='#BBFFFF'))
bar = Bar()
bar.add_xaxis(x)
bar.add_yaxis("平均重量", y)
bar.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌平均重量"),
                    visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
                if float(i[1]) > 2000:
                    d[t] = d.get(t, 0) + float(i[1])
                    e[t] = e.get(t, 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])
bar1 = Bar()
bar1.add_xaxis(x)
bar1.add_yaxis("平均价格", y)
bar1.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar1.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar1.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if len(i[3]) > 1 and '18GB' not in i[3]:
        d[i[3]] = d.get(i[3], 0) + float(i[1])
        e[i[3]] = e.get(i[3], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].replace('运行内存：', ''))
    y.append(i[1])
bar2 = Bar()
bar2.add_xaxis(x)
bar2.add_yaxis("平均价格", y)
bar2.set_global_opts(title_opts=opts.TitleOpts(title="手机运行内存平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar2.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar2.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if len(i[4]) > 1:
        if float(i[1]) > 2000:
            d[i[4]] = d.get(i[4], 0) + float(i[1])
            e[i[4]] = e.get(i[4], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[1:11]:
    x.append(i[0].replace('CPU型号：', ''))
    y.append(i[1])

bar3 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar3.add_xaxis(x)
bar3.add_yaxis("平均价格", y)
bar3.set_global_opts(title_opts=opts.TitleOpts(title="手机cpu型号平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar3.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar3.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if len(i[5]) > 1:
        d[i[5]] = d.get(i[5], 0) + float(i[1])
        e[i[5]] = e.get(i[5], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].replace('前摄主摄像素：', ''))
    y.append(i[1])

bar4 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar4.add_xaxis(x)
bar4.add_yaxis("平均价格", y)
bar4.set_global_opts(title_opts=opts.TitleOpts(title="手机前摄主像素平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar4.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar4.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if len(i[6]) > 1:
        if float(i[1]) > 1000:
            d[i[6]] = d.get(i[6], 0) + float(i[1])
            e[i[6]] = e.get(i[6], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].replace('后摄主摄像素：', ''))
    y.append(i[1])
bar5 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar5.add_xaxis(x)
bar5.add_yaxis("平均价格", y)
bar5.set_global_opts(title_opts=opts.TitleOpts(title="手机后摄主像素平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar5.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar5.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            if len(i[5]) > 1:

                if '万' in i[5]:
                    ll = i[5].replace('前摄主摄像素：', '').replace('万像素', '')
                    e[t] = e.get(t, 0) + 1
                    d[t] = d.get(t, 0) + float(ll)
                if '亿' in i[5]:
                    ll = i[5].replace('前摄主摄像素：', '').replace('亿像素', '')
                    ll = float(ll) * 10000
                    e[t] = e.get(t, 0) + 1
                    d[t] = d.get(t, 0) + float(ll)
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:15]:
    x.append(i[0])
    y.append(i[1])
bar6 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar6.add_xaxis(x)
bar6.add_yaxis("像素/万", y)
bar6.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌平均前摄主像素"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar6.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar6.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            if len(i[6]) > 1:
                if '万' in i[6]:
                    ll = i[6].replace('后摄主摄像素：', '').replace('万像素', '')
                    e[t] = e.get(t, 0) + 1
                    d[t] = d.get(t, 0) + float(ll)
                if '亿' in i[6]:
                    ll = i[6].replace('后摄主摄像素：', '').replace('亿像素', '')
                    ll = float(ll) * 10000
                    e[t] = e.get(t, 0) + 1
                    d[t] = d.get(t, 0) + float(ll)
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:15]:
    x.append(i[0])
    y.append(i[1])
bar7 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar7.add_xaxis(x)
bar7.add_yaxis("像素/万", y)
bar7.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌平均后摄主像素"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar7.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar7.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if 15 > len(i[7]) > 4 and '分辨率' in i[7]:
        if float(i[1]) > 1000:
            d[i[7]] = d.get(i[7], 0) + float(i[1])
            e[i[7]] = e.get(i[7], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].split('：')[1])
    y.append(i[1])

bar8 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar8.add_xaxis(x)
bar8.add_yaxis("平均价格", y)
bar8.set_global_opts(title_opts=opts.TitleOpts(title="手机分辨率平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar8.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar8.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if float(i[1]) > 1000:
        if len(i[8]) > 0 and '其他' not in i[8] and '以下' not in i[8]:
            d[i[8]] = d.get(i[8], 0) + float(i[1])
            e[i[8]] = e.get(i[8], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].split('：')[1])
    y.append(i[1])

bar9 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar9.add_xaxis(x)
bar9.add_yaxis("平均价格", y)
bar9.set_global_opts(title_opts=opts.TitleOpts(title="机身内存平均价格"),
                     visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar9.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar9.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj:
    if len(i[10]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
            d[i[10]] = d.get(i[10], 0) + float(i[-1])
            e[i[10]] = e.get(i[10], 0) + 1
for i in d:
    age = round(d[i], 0)
    if '小米' in i:
        age = age - 3000000
    c.append([i[:-3], age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:8]:
    x.append(i[0])
    y.append(i[1])

bar10 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar10.add_xaxis(x)
bar10.add_yaxis("数量", y)
bar10.set_global_opts(title_opts=opts.TitleOpts(title="店铺数前n"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar10.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar10.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
qr = 0
for i in bg_sj:
    if len(i[10]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
            qr = qr + float(i[-1])
            d[i[10]] = d.get(i[10], 0) + float(i[-1])
            e[i[10]] = e.get(i[10], 0) + 1
for i in d:
    age = round(d[i], 0)

    c.append([i[:-3], age])
c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    qr = qr - i[1]
    if '小米' in i[0]:
        x.append(i[0])
        y.append(i[1] - 3000000)
    else:
        x.append(i[0])
        y.append(i[1])
x.append('其他')
y.append(qr)
pie2 = Pie()

pie2.add("", [list(z) for z in zip(x, y)]
         , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
pie2.set_global_opts(
    title_opts=opts.TitleOpts(title="店铺前n", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
pie2.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-1])

for i in d:
    age = round(e[i], 0)
    if '小米' in i:
        age = age - 3000000
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar11 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar11.add_xaxis(x)
bar11.add_yaxis("数量", y)
bar11.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌好评数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar11.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar11.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in bbb:
    for i in bg_sj:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-2])

for i in d:
    age = round(e[i], 0)
    if '小米' in i:
        age = age - 11000000
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar12 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar12.add_xaxis(x)
bar12.add_yaxis("数量", y)
bar12.set_global_opts(title_opts=opts.TitleOpts(title="手机品牌评论数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar12.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar12.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

www = ['联想', '华硕', '宏碁', '清华同方', '神舟', '苹果', '戴尔', '惠普', '三星', '索尼', '海尔', 'ThinkPad', '华为', '外星人', '雷神', 'a豆', '小米',
       '荣誉', '明基', '大众', '长城', '方正', '紫光', '浪潮', 'TCL', '海尔', '海信', '七喜', '澳柯马', '同创', '新蓝', '酷睿', '武极', '机械师',
       '爱尔游', '微软']
bg_sj1 = dq_mysql('sj_dn1')
strs1 = ''
for i in bg_sj1:
    strs1 = strs1 + i[0]

di8 = {}
text1 = trans_CN(strs1)
for t in www:
    ts = 0
    for i in text1.split(' '):
        if t in i:
            ts = ts + 1
    di8[t] = ts
words1 = []
for i in di8:
    words1.append((i, di8[i]))


def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
            .add("", words1, word_size_range=[20, 100])
            .set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌词云"))
    )
    return c


wd1 = wordcloud_base()

di4 = {}
c4 = []
for t in www:
    for i in bg_sj1:
        if t in i[0]:
            di4[t] = di4.get(t, 0) + 1
for i in di4:
    c4.append([i, di4[i]])


def px(f):
    return f[1]


c4.sort(key=px, reverse=True)
cate = []
data = []
age = 0
for i in c4[:10]:
    cate.append(i[0])
    data.append(i[1])
    age = age + i[1]
cate.append('其他')
data.append(len(bg_sj1) - age)
pie1 = Pie()

pie1.add("", [list(z) for z in zip(cate, data)]
         , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
pie1.set_global_opts(
    title_opts=opts.TitleOpts(title="电脑品牌饼图", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
pie1.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
for t in www:
    for i in bg_sj1:
        if t in i[0]:
            if '手机' not in i[0] and '数据线' not in i[0] and '鼠标' not in i[0] and '充电宝' not in i[0] and '支架' not in i[
                0] and '包' not in i[0]:
                d[t] = d.get(t, 0) + float(i[1])
                e[t] = e.get(t, 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar13 = Bar()
bar13.add_xaxis(x)
bar13.add_yaxis("平均价格", y)
bar13.set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar13.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar13.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
w1 = []
for t in www:
    for i in bg_sj1:
        if len(i[2]) > 6:
            if t in i[0]:
                zl = i[2].replace('商品毛重：', '').replace('g', '')
                if 'k' in zl:
                    zl = float(zl.replace('k', '')) * 1000
                    if zl < 10000:
                        d[t] = d.get(t, 0) + zl
                        e[t] = e.get(t, 0) + 1
                elif 'g' in zl:
                    zl = float(zl)
                    if zl < 10000:
                        d[t] = d.get(t, 0) + zl
                        e[t] = e.get(t, 0) + 1
for i in d:
    if e[i] > 50:
        age = round(d[i] / e[i], 2)
        c.append([i, age])


def px(f):
    return f[1]


c.sort(key=px, reverse=True)
x = []
y = []
for i in c[2:12]:
    x.append(i[0])
    y.append(i[1])

bar14 = Bar()
bar14.add_xaxis(x)
bar14.add_yaxis("平均重量/克", y)
bar14.set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌平均重量"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar14.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar14.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
w1 = []
for i in bg_sj1:
    if len(i[3]) > 1:
        d[i[3]] = d.get(i[3], 0) + 1

for i in d:
    if '其他' not in i:
        c.append([i.replace('颜色：', ''), d[i]])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])

bar15 = Bar()
bar15.add_xaxis(x)
bar15.add_yaxis("颜色数量", y)
bar15.set_global_opts(title_opts=opts.TitleOpts(title="电脑颜色数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar15.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar15.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in www:
    for i in bg_sj1:
        if t in i[0]:
            if len(i[4]) > 1:
                if '其他' not in i[4]:
                    ll = i[4].replace('屏幕刷新率：', '').replace('Hz', '').replace('及以上', '')
                    e[t] = e.get(t, 0) + 1
                    d[t] = d.get(t, 0) + float(ll)
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:15]:
    x.append(i[0])
    y.append(i[1])
bar16 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar16.add_xaxis(x)
bar16.add_yaxis("Hz", y)
bar16.set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌平均屏幕刷新率"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar16.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar16.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj1:
    d[i[4]] = d.get(i[4], 0) + float(i[1])
    e[i[4]] = e.get(i[4], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i.replace('屏幕刷新率：', ''), age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])

bar17 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar17.add_xaxis(x)
bar17.add_yaxis("平均价格", y)
bar17.set_global_opts(title_opts=opts.TitleOpts(title="电脑屏幕刷新率平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar17.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar17.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
w1 = []
for i in bg_sj1:
    if len(i[5]) > 1:
        d[i[5]] = d.get(i[5], 0) + 1

for i in d:
    if '其他' not in i:
        c.append([i.replace('厚度：', ''), d[i]])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])

bar18 = Bar()
bar18.add_xaxis(x)
bar18.add_yaxis("厚度数量", y)
bar18.set_global_opts(title_opts=opts.TitleOpts(title="电脑厚度数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar18.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar18.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj1:
    wr = i[8].split('，')
    if len(i[8]) > 1 and len(wr) < 2:
        d[i[8]] = d.get(i[8], 0) + float(i[1])
        e[i[8]] = e.get(i[8], 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i.replace('处理器：', ''), age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[2:9]:
    x.append(i[0])
    y.append(i[1])

bar19 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar19.add_xaxis(x)
bar19.add_yaxis("平均价格", y)
bar19.set_global_opts(title_opts=opts.TitleOpts(title="电脑处理器平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar19.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar19.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

bg_sj2 = dq_mysql('sj_dn2')
bg_dn = dq_mysql('sj_dn3')
d = {}
e = {}
c = []
for t in www:
    for i in bg_sj2:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-1])

for i in d:
    age = round(e[i], 0)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar20 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar20.add_xaxis(x)
bar20.add_yaxis("数量", y)
bar20.set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌好评数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar20.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar20.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_dn:
    if len(i[1]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0] and '网线' not in i[0] and '路由器' not in i[0]:
            if '绿联'not in i[1] and '山泽'not in i[1] and 'APPLE翔合'not in i[1] and 'TP-LINK京东自营'not in i[1] and '金士顿京东自营'not in i[1]:
                if '得力京'not in i[1] and '雷柏京'not in i[1] and '飞利浦'not in i[1] and 'JRC京'not in i[1]:
                    d[i[1]] = d.get(i[1], 0) + float(i[-2])
                    e[i[1]] = e.get(i[1], 0) + 1
for i in d:
    age = round(d[i], 0)
    c.append([i[:-3], age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])
print(x)
print(y)
bardn = Bar(init_opts=opts.InitOpts(width='1500px'))
bardn.add_xaxis(x)
bardn.add_yaxis("数量", y)
bardn.set_global_opts(title_opts=opts.TitleOpts(title="店铺数前n"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bardn.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bardn.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
qr = 0
for i in bg_dn:
    if len(i[1]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0] and '网线' not in i[0] and '路由器' not in i[0]:
            if '绿联'not in i[1] and '山泽'not in i[1] and 'APPLE翔合'not in i[1] and 'TP-LINK京东自营'not in i[1] and '金士顿京东自营'not in i[1]:
                if '得力京'not in i[1] and '雷柏京'not in i[1] and '飞利浦'not in i[1] and 'JRC京'not in i[1]:
                    qr = qr + float(i[-2])
                    d[i[1]] = d.get(i[1], 0) + float(i[-2])
                    e[i[1]] = e.get(i[1], 0) + 1
for i in d:
    age = round(d[i], 0)
    c.append([i[:-3], age])
c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    qr = qr - i[1]
    x.append(i[0])
    y.append(i[1])
x.append('其他')
y.append(qr)
piedn = Pie()

piedn.add("", [list(z) for z in zip(x, y)]
          , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
piedn.set_global_opts(
    title_opts=opts.TitleOpts(title="店铺前n", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
piedn.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
for t in www:
    for i in bg_sj2:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0]:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-2])

for i in d:
    age = round(e[i], 0)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar21 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar21.add_xaxis(x)
bar21.add_yaxis("数量", y)
bar21.set_global_opts(title_opts=opts.TitleOpts(title="电脑品牌评论数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar21.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar21.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

qqq = ['品弘', '酷比魔方', '华硕', 'iPad', '华为', '微软', '联想', '荣耀', '三星', '台电', '小米', '酷派', '中柏', '魅族', '同方', '方正', '紫光', '浪潮',
       'TCL', '海尔', '海信', '七喜', '澳柯马', '同创', '新蓝', '酷睿', '武极', '机械师',
       '爱尔游']

bg_sj3 = dq_mysql('sj_pb')

strs2 = ''
for i in bg_sj3:
    strs2 = strs2 + i[0]


def trans_CN(text):
    word_list = jieba.cut(text)
    result = " ".join(word_list)
    return result


di18 = {}
text = trans_CN(strs2)
for t in qqq:
    ts = 0
    for i in text.split(' '):
        if t in i:
            ts = ts + 1
    di18[t] = ts
words = []
for i in di18:
    words.append((i, di18[i]))


def wordcloud_base() -> WordCloud:
    c = (
        WordCloud()
            .add("", words, word_size_range=[30, 150])
            .set_global_opts(title_opts=opts.TitleOpts(title="平板品牌词云"))
    )
    return c


wd2 = wordcloud_base()

di4 = {}
c4 = []
for t in qqq:
    for i in bg_sj3:
        if t in i[0]:
            di4[t] = di4.get(t, 0) + 1
for i in di4:
    c4.append([i, di4[i]])


def px(f):
    return f[1]


c4.sort(key=px, reverse=True)
cate = []
data = []
age = 0
for i in c4[:8]:
    cate.append(i[0])
    data.append(i[1])
    age = age + i[1]
cate.append('其他')
data.append(len(bg_sj) - age)
pie3 = Pie()

pie3.add("", [list(z) for z in zip(cate, data)]
         , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
pie3.set_global_opts(
    title_opts=opts.TitleOpts(title="平板品牌饼图", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
pie3.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
for t in qqq:
    for i in bg_sj3:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '充电' not in i[0] and '接口' not in i[0] and '连接器' not in i[
                0] and float(i[1]) > 500:
                d[t] = d.get(t, 0) + float(i[1])
                e[t] = e.get(t, 0) + 1
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar22 = Bar()
bar22.add_xaxis(x)
bar22.add_yaxis("平均价格", y)
bar22.set_global_opts(title_opts=opts.TitleOpts(title="平板品牌平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar22.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar22.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
w1 = []
for t in qqq:
    for i in bg_sj3:
        if len(i[2]) > 2:
            if t in i[0]:
                zl = i[2].replace('商品毛重：', '').replace('g', '')
                if 'k' in zl:
                    zl = float(zl.replace('k', '')) * 1000
                    if 200 < zl < 2000:
                        d[t] = d.get(t, 0) + zl
                        e[t] = e.get(t, 0) + 1
                elif 'g' in zl:
                    zl = float(zl)
                    if 200 < zl < 2000:
                        d[t] = d.get(t, 0) + zl
                        e[t] = e.get(t, 0) + 1
for i in d:
    if e[i] > 50:
        age = round(d[i] / e[i], 2)
        c.append([i, age])


def px(f):
    return f[1]


c.sort(key=px, reverse=True)
x = []
y = []
for i in c:
    x.append(i[0])
    y.append(i[1])

bar23 = Bar()
bar23.add_xaxis(x)
bar23.add_yaxis("平均重量/克", y)
bar23.set_global_opts(title_opts=opts.TitleOpts(title="平板品牌平均重量"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar23.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar23.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[3]) > 1 and '运行内存：' in i[3]:
        d[i[3]] = d.get(i[3], 0) + float(i[1])
        e[i[3]] = e.get(i[3], 0) + 1
for i in d:
    if '其他' not in i and '无' not in i:
        age = round(d[i] / e[i], 2)
        c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].replace('运行内存：', ''))
    y.append(i[1])

bar24 = Bar()
bar24.add_xaxis(x)
bar24.add_yaxis("平均价格", y)
bar24.set_global_opts(title_opts=opts.TitleOpts(title="平板运行内存平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar24.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar24.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[4]) > 1 and '可扩展容量：' in i[4]:
        d[i[4]] = d.get(i[4], 0) + float(i[1])
        e[i[4]] = e.get(i[4], 0) + 1
    if '512' in i[4] or '128' in i[4]:
        d[i[4]] = d.get(i[4], 0) + 1000
for i in d:
    if '其他' not in i and '无' not in i:
        age = round(d[i] / e[i], 2)
        c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0].replace('可扩展容量：', '').replace('最大支持', ''))
    y.append(i[1])

bar24 = Bar()
bar24.add_xaxis(x)
bar24.add_yaxis("平均价格", y)
bar24.set_global_opts(title_opts=opts.TitleOpts(title="平板可扩展容量平均价格"))

d = {}
e = {}
c = []
for t in www:
    for i in bg_sj3:
        if t in i[0]:
            if len(i[5]) > 1:
                if '其他' not in i[5] and '以' not in i[5] and '无' not in i[5] and 2 < len(i[5]) < 10:
                    wi = i[5].replace('屏幕尺寸：', '').replace('英寸', '').split('-')[-1]
                    ll = i[5].replace('屏幕尺寸：', '').replace('英寸', '')
                    if 5 < float(ll) < 25:
                        try:
                            e[t] = e.get(t, 0) + 1
                            d[t] = d.get(t, 0) + float(ll)
                        except:
                            e[t] = e.get(t, 0) + 1
                            d[t] = d.get(t, 0) + float(wi)
for i in d:
    age = round(d[i] / e[i], 2)
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c:
    x.append(i[0])
    y.append(i[1])
bar25 = Bar()
bar25.add_xaxis(x)
bar25.add_yaxis("Hz", y)
bar25.set_global_opts(title_opts=opts.TitleOpts(title="平板品牌屏幕尺寸"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar25.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar25.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[6]) > 2 and '其他' not in i[6]:
        d[i[6]] = d.get(i[6], 0) + 1

for i in d:
    ''.replace('，教育电视', '')
    c.append([i.replace('类型：', '').replace('，4K超清', '').replace('，教育电视', ''), d[i]])

c.sort(key=px, reverse=True)
x = []
y = []
w = 0
for i in c:
    if i[0] not in x:
        w = w + 1
        x.append(i[0])
        y.append(i[1])
    if w == 9:
        break

bar26 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar26.add_xaxis(x)
bar26.add_yaxis("数量", y)
bar26.set_global_opts(title_opts=opts.TitleOpts(title="平板类型数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar26.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar26.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if 30 > len(i[7]) > 2 and '其他' not in i[7]:
        d[i[7].lower()] = d.get(i[7].lower(), 0) + 1

for i in d:
    c.append([i.replace('系统：', '').replace('，4K超清', '').replace('，教育电视', ''), d[i]])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])

bar27 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar27.add_xaxis(x)
bar27.add_yaxis("数量", y)
bar27.set_global_opts(title_opts=opts.TitleOpts(title="平板系统数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar27.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar27.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[7]) > 1 and '系统：' in i[7]:
        d[i[7]] = d.get(i[7], 0) + float(i[1])
        e[i[7]] = e.get(i[7], 0) + 1
for i in d:
    if '其他' not in i and '无' not in i:
        age = round(d[i] / e[i], 2)
        c.append([i.replace('系统：', '').replace(' 带Office', ''), age])

c.sort(key=px, reverse=True)

x = []
y = []
for i in c[1:9]:
    x.append(i[0])
    y.append(i[1])

bar28 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar28.add_xaxis(x)
bar28.add_yaxis("平均价格", y)
bar28.set_global_opts(title_opts=opts.TitleOpts(title="平板系统平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar28.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar28.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[8]) > 1 and '处理器：' in i[8]:
        d[i[8]] = d.get(i[8], 0) + float(i[1])
        e[i[8]] = e.get(i[8], 0) + 1
for i in d:
    if '其他' not in i and '无' not in i:
        age = round(d[i] / e[i], 2)
        c.append([i.replace('处理器：', '').replace(' 带Office', ''), age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[1:11]:
    x.append(i[0])
    y.append(i[1])

bar29 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar29.add_xaxis(x)
bar29.add_yaxis("平均价格", y)
bar29.set_global_opts(title_opts=opts.TitleOpts(title="平板处理器平均价格"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar29.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar29.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for i in bg_sj3:
    if len(i[-3]) > 2 and '其他' not in i[-3]:
        d[i[-3]] = d.get(i[-3], 0) + 1

for i in d:
    c.append([i.replace('颜色：', ''), d[i]])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar30 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar30.add_xaxis(x)
bar30.add_yaxis("数量", y)
bar30.set_global_opts(title_opts=opts.TitleOpts(title="平板颜色数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar30.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar30.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
for t in qqq:
    for i in bg_sj3:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '充电' not in i[0] and '接口' not in i[0] and '连接器' not in i[
                0] and float(i[1]) > 200:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-2])

for i in d:
    age = round(e[i], 0)
    if '小米' in i:
        age = age - 20000000
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])

bar31 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar31.add_xaxis(x)
bar31.add_yaxis("数量", y)
bar31.set_global_opts(title_opts=opts.TitleOpts(title="平板品牌评论数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar31.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar31.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

bg_pb = dq_mysql('sj_pb1')

d = {}
e = {}
c = []
for i in bg_pb:
    if len(i[1]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0] and '灭菌'not in i[0] and '口罩'not in i[0]:
            if 'XAXR医疗' not in i[1] and '洁云京东自营' not in i[1] and '百家好世' not in i[1] and '稳健京东自营' not in i[1]and '维德（WELLDAY）京东自营' not in i[1] and '亿色(ESR)京东自营' not in i[1]:
                d[i[1]] = d.get(i[1], 0) + float(i[-2])
                e[i[1]] = e.get(i[1], 0) + 1
for i in d:
    age = round(d[i], 0)
    c.append([i[:-3], age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    x.append(i[0])
    y.append(i[1])

barpb = Bar(init_opts=opts.InitOpts(width='1500px'))
barpb.add_xaxis(x)
barpb.add_yaxis("数量", y)
barpb.set_global_opts(title_opts=opts.TitleOpts(title="店铺数前n"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
barpb.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
barpb.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))

d = {}
e = {}
c = []
qr = 0
for i in bg_pb:
    if len(i[1]) > 0:
        if '耳机' not in i[0] and '数据线' not in i[0] and '手表' not in i[0] and '充电宝' not in i[0] and '灭菌'not in i[0] and '口罩'not in i[0]:
            if 'XAXR医疗' not in i[1] and '洁云京东自营' not in i[1] and '百家好世' not in i[1] and '稳健京东自营' not in i[1]and '维德（WELLDAY）京东自营' not in i[1] and '亿色(ESR)京东自营' not in i[1]:
                qr = qr + float(i[-2])
                d[i[1]] = d.get(i[1], 0) + float(i[-2])
                e[i[1]] = e.get(i[1], 0) + 1
for i in d:
    age = round(d[i], 0)

    c.append([i[:-3], age])
c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:5]:
    qr = qr - i[1]
    x.append(i[0])
    y.append(i[1])
x.append('其他')
y.append(qr)
piepb = Pie()

piepb.add("", [list(z) for z in zip(x, y)]
          , label_opts=opts.LabelOpts(
        position="outside",
        formatter="{d}%", ))
piepb.set_global_opts(
    title_opts=opts.TitleOpts(title="店铺前n", pos_left='70%'),
    legend_opts=opts.LegendOpts(
        type_="scroll"
        , pos_top="20%"
        , pos_left="80%"
        , orient="vertical"
    ),
)
piepb.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

d = {}
e = {}
c = []
for t in qqq:
    for i in bg_sj3:
        if t in i[0]:
            if '耳机' not in i[0] and '数据线' not in i[0] and '充电' not in i[0] and '接口' not in i[0] and '连接器' not in i[
                0] and float(i[1]) > 200:
                d[t] = d.get(t, 0) + 1
                e[t] = e.get(t, 0) + int(i[-1])

for i in d:
    age = round(e[i], 0)
    if '小米' in i:
        age = age - 15000000
    c.append([i, age])

c.sort(key=px, reverse=True)
x = []
y = []
for i in c[:10]:
    x.append(i[0])
    y.append(i[1])
page = Page(layout=Page.DraggablePageLayout)
bar32 = Bar(init_opts=opts.InitOpts(width='1500px'))
bar32.add_xaxis(x)
bar32.add_yaxis("数量", y)
bar32.set_global_opts(title_opts=opts.TitleOpts(title="平板品牌好评数"),
                      visualmap_opts=opts.VisualMapOpts(max_=max(y), min_=min(y)))
bar32.set_series_opts(markpoint_opts=opts.MarkPointOpts(
    data=[opts.MarkPointItem(type_="max", name="最大值"),
          opts.MarkPointItem(type_="min", name="最小值")])
)
bar32.set_series_opts(markline_opts=opts.MarkLineOpts(
    data=[opts.MarkLineItem(type_="average", name="平均值")]
))
pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
page1 = Page(layout=Page.DraggablePageLayout)
page2 = Page(layout=Page.DraggablePageLayout)
page.add(wd, pie, bar, bar1, bar2, bar3, bar4, bar5, bar6, bar7, bar8, bar9, bar10, pie2, bar11, bar12)
page1.add(wd1, pie1,
          bar13,
          bar14, bar15, bar16, bar17, bar18, bar19, bar20, bardn, piedn, bar21)
page2.add(wd2, pie3, bar22, bar23, bar24, bar25, bar26, bar27
          , bar28, bar29, bar30, bar31, barpb, piepb, bar32)
page.render('D:\index.html')
page1.render('D:\index1.html')
page2.render('D:\index2.html')
