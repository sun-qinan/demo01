from pyecharts.charts import Bar, Page
import pymysql


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
    # db.close()


lis = []
bg_sj = dq_mysql('sj_shouji')
bg_sj1 = dq_mysql('sj_dn1')
bg_sj2 = dq_mysql('sj_pb')
data = {}
for i in bg_sj:
    lis.append(i)
for i in bg_sj1:
    lis.append(i)
for i in bg_sj2:
    lis.append(i)
print(len(lis))
q, w, e = 0, 0, 0
for i in lis:
    if '电脑' in i[0]:
        print(i[0])
        q = q + 1
    elif '手机' in i[0]:
        w = w + 1
    elif '平板' in i[0]:
        e = e + 1
lis1 = ['手机', '电脑', '平板']
lis2 = [w, q, e]
print(q, w, e)
page = Page(layout=Page.DraggablePageLayout)
bar = Bar()
bar.add_xaxis(lis1)
bar.add_yaxis("数量", lis2)
bar.render('qwe.html')
