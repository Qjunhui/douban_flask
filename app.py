from flask import Flask,render_template
import sqlite3 # 数据库

import jieba # 分词pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple jieba
from matplotlib import pyplot as plt # 绘图，数据可视化
from wordcloud import WordCloud # 词云
from PIL import Image # 图片处理
import numpy as np # 矩阵运算

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# index
@app.route('/index')
def index():
    return home()

# movie
@app.route('/movie')
def movie():
    dataList = []
    con = sqlite3.connect('douban.db')
    cur = con.cursor()
    sql = 'select * from movie250'
    data = cur.execute(sql)
    for item in data:
        dataList.append(item)
    cur.close()
    con.close()

    return render_template('movie.html',movies = dataList)

# score
@app.route('/score')
def score():
    score = [] # 评分
    scoreNum = [] # 评分的数量
    con = sqlite3.connect('douban.db')
    cur = con.cursor()
    sql = 'select rating,count(rating) from movie250 group by rating'
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        scoreNum.append(item[1])

    cur.close()
    con.close()
    return render_template('score.html',score=score,scoreNum=scoreNum)

# word
@app.route('/word')
def word():
    # 1. 词云所需的文字
    con = sqlite3.connect('douban.db')
    cur = con.cursor()
    sql = 'select inq from movie250'
    data = cur.execute(sql)
    text = ''
    for item in data:
        text += item[0]
    cur.close()
    con.close()

    # 2.分词
    cut = jieba.cut(text)
    string = ' '.join(cut)

    # 3.背景图片
    img = Image.open(r'./static/assets/img/strawberry.jpeg')
    imgArray = np.array(img)  # 将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=imgArray,
        font_path='/Library/Fonts/Songti.ttc'
    )
    wc.generate_from_text(string)

    # 4.绘图
    flg = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    # plt.show() # 显示生成的词云图片

    # 输出词云文件到文件
    plt.savefig('./static/assets/img/douban.jpg')

    return render_template('word.html')

# team
@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run()