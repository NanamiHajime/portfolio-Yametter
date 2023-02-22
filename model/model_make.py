# -*- coding: utf-8 -*-
import collections
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction import DictVectorizer
#二値分類モデルの学習 確率的勾配降下法
from sklearn.linear_model import SGDClassifier

VX=DictVectorizer()
VY=LabelEncoder()

#.を削除してリストにする
def tokenize(s):
  return [t.rstrip('.') for t in s.split(' ')]

  #辞書型で何個文字があるか記録
def vectorize(tokens):
  return collections.Counter(tokens)

def readiter(fi):
  for line in fi:
    fields=line.strip('\n').split('\t')
    x=vectorize(tokenize(fields[1]))
    y=fields[0]
    yield x, y

#モデルを作る
def model_make():
  with open('./model/dataset.txt', encoding="utf-8") as fi:
    D=[d for d in readiter(fi)]

  #単語の出現頻度
  D[6]

  #train data:90% test data:10%
  Dtrain, Dtest=train_test_split(D, test_size=0.2, random_state=0)

  '''
  #特徴をキー、値をバリュートする辞書オブジェクトから
  #特徴オブジェクトに変換する
  0から始めるID番号を割り振っていく
  '''

  Xtrain=VX.fit_transform(d[0] for d in Dtrain)
  Ytrain=VY.fit_transform([d[1] for d in Dtrain])
  Xtest=VX.transform([d[0] for d in Dtest])
  Ytest=VY.transform([d[1] for d in Dtest])

  Dtrain[7]

  '''
  #疎ベクトルとして保存されている
  '''
  #print(Xtrain[7])


  #ロジスティクス回帰モデルを学習する
  model=SGDClassifier(loss="log")
  #fit関数に訓練データを渡してモデルのパラメータを学習させる
  model.fit(Xtrain, Ytrain)

  return model

def model_suiron(msg):
  model=model_make()
  #print(vectorize(tokenize(msg)))
  #print(VX.transform(vectorize(tokenize(msg))))

  result=model.predict(VX.transform(vectorize(tokenize(msg))))
  # recent_stressに モデルはNEGATIVEを返した場合
  if result==0:
      return "NEGATIVE"
  else:
      return "POSITIVE"
