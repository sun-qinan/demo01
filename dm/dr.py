import pymysql

try:
    db = pymysql.connect(host='localhost', user='root', password='', database='text', charset='utf8')
    print('数据库连接成功')
    cur = db.cursor()
    sql = 'INSERT INTO sj_pb1(名称,店铺名,评论数,好评数) VALUE(%s,%s,%s,%s)'
    with open('zzsj电脑11.txt', 'r', encoding='utf-8') as f:
        aa = f.read().split('\n')
    qw = 0
    for bb in aa:
        qw = qw + 1
        ww = bb.split(',')
        if len(ww[-2]) > 0 and len(ww[-1]) > 0:
            value = (ww[-5], ww[-3], ww[-2].replace('1.', ''), ww[-1].replace('1.', ''))
            cur.execute(sql, value)
            db.commit()
        print(qw)
    print('添加成功')
except pymysql.Error as e:
    print('数据库添加失败' + str(e))
    db.rollback()
db.close()
