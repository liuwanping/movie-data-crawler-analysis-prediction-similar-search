import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import jieba


stopwords = {}

def stopword(filename = ''):
    global stopwords
    f = open(filename, 'rb')
    line = f.readline().rstrip()
    while line:
        stopwords.setdefault(line, 0)
        stopwords[line.decode('utf-8')] = 1
        line = f.readline().rstrip()
    f.close()
stopword(filename = 'F:/anaconda/Scripts/pachong/data/stopwords.txt')


with open ('F:/anaconda/Scripts/pachong/data/testdata/comment_data.txt',encoding="UTF-8") as f:
    text = f.readlines()
    text = r''.join(str(text))
    seg_generator = jieba.cut(text)
    seg_list = [i for i in seg_generator if i not in stopwords]
    seg_list = [i for i in seg_list if i != u' ']
    seg_list = r' '.join(seg_list)
# 词云
wordcloud = WordCloud(font_path='C:/Windows/Fonts/simsun.ttc', background_color="white", margin=5, width=1800, height=800) 
wordcloud = wordcloud.generate(seg_list)
#画图
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()