# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# 加载数据集
df = pd.read_csv("F:/anaconda/Scripts/pachong/data/data.csv",encoding = 'gb18030')


# 数据预处理，将非数值型数据转换为数值型
columnsToEncode = list(df.select_dtypes(include=["category","object",'number']))
le = LabelEncoder()
for feature in columnsToEncode:
    try:
        df[feature] = le.fit_transform(df[feature].astype(str))
    except:
        print('Error encoding ' + feature)

X = df
y = X['评分']
X = X.drop(['电影名','评分','评论','下载链接','简介'], axis=1)


# 数据分割，90%作为训练集，10%作为测试集
scaler=StandardScaler()
X = scaler.fit_transform(X)
y = np.array(y).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=33)


# 用随机深林模型来预测
treenum = range(500)
accuracy = []
for i in treenum:
    clf = RandomForestClassifier(n_estimators=100)
    clf = clf.fit(X_train, y_train)
    clf_y_predict = clf.predict(X_test)
    accuracy.append(accuracy_score(y_test, clf_y_predict))
    print(accuracy_score(y_test, clf_y_predict))

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

plt.plot(treenum,accuracy)
plt.title('准确率随树的个数变化情况')
plt.xlabel('树的个数')

plt.ylabel('准确率')
plt.grid() 
plt.savefig('F:/anaconda/Scripts/pachong/figures/准确率随树的个数变化情况.png')
plt.show()

