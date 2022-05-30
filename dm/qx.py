with open('手机数据.csv', 'r', encoding='utf-8') as f:
    aa = f.read().split('\n')
cc = []
for i in aa:
    bb = i.split(',')
    nc = ''
    fbn = ''
    qs = ''
    hs = ''
    yxnc = ''
    gpu = ''
    zl = ''
    name = ''
    for t in bb:
        if '机身内存' in t:
            nc = t
        if '分辨率' in t:
            fbn = t
        if '前摄主摄' in t:
            qs = t
        if '后摄主' in t:
            hs = t
        if '运行内存' in t:
            yxnc = t
        if 'CPU型号' in t:
            gpu = t
        if '商品毛重' in t:
            zl = t
        if '商品名称' in t:
            name = t
    sj = name + ',' + bb[0] + ',' + zl + ',' + yxnc + ',' + gpu + ',' + qs + ',' + hs + ',' + fbn + ',' + nc + ',' + bb[
        -1] + ','
    with open('手机sj.csv', 'a+', encoding='utf-8') as f1:
        f1.write(sj + '\n')
    print(sj)
