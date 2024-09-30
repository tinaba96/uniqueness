#from fastapi import FastAPI, HTTPException
#import datetime
#from model import get_data_from_firestore

import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import MeCab
import pandas as pd
import numpy as np

import firebase_admin
from firebase_admin import credentials, firestore

texts = []

try:
    #firebase_admin.initialize_app()
    cred = credentials.Certificate('/Users/takahiroinaba/src/github/tinaba96/uniqueness/firestore.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    #users_ref = db.collection(u'test')
    datas = db.collection(u'ai-analysis')
    docs = datas.get()

    for doc in docs:
        #print(f'Document ID: {doc.id}')
        data = doc.to_dict()  # フィールドの値を辞書形式で取得

        # フィールドごとの値を出力
        for field, value in data.items():
            #print(f'{field}: {value}')
            texts.append(value)


except Exception as e:
    print('error')
    print(e)

print(value)

def text_to_words(text):
    # tagger = MeCab.Tagger('-O chasen')
    tagger = MeCab.Tagger(f'-O chasen -d {dic_path}')
    chunks = tagger.parse(text).splitlines()
    words = []
    for chunk in chunks:
        line = chunk.split('\t')
        if len(line) > 3:
            if line[0] != '<DATE>' and line[3] != '名詞-数':  # 日付はあらかじめ<DATE>に置換しておいた
                words.append(line[2])
    return words


def calc_vecs(docs):
  # vectorizer = TfidfVectorizer(analyzer=text_to_words)
  vectorizer = TfidfVectorizer(analyzer=mecab_sep)
  vecs = vectorizer.fit_transform(docs)
  return vecs.toarray()

#m = MeCab.Tagger(f'-O chasen -d {dic_path}')
m = MeCab.Tagger("-Owakati")

def mecab_sep(text):
    node = m.parseToNode(text)

    words_list = []

    while node:
        if node.feature.split(",")[0] == "名詞":
            words_list.append(node.surface)
        elif node.feature.split(",")[0] == "動詞":
            words_list.append(node.feature.split(",")[6])
        elif node.feature.split(",")[0] == "形容詞":
            words_list.append(node.feature.split(",")[6])
        # else:
        #     words_list.append(node.surface)
        node = node.next

    return words_list

pd_texts = pd.DataFrame(texts, columns=['テキスト'])

all_vecs = calc_vecs(pd_texts['テキスト'])


#print(all_vecs)


input_data = '評価システムがちゃんとしておらず、社員に適切な評価がされていない。'
pd_texts = pd.DataFrame([input_data]+texts, columns=['テキスト'])

tot_vecs = calc_vecs(pd_texts['テキスト'])


similarity = cosine_similarity([tot_vecs[0]], tot_vecs[1:])
self_similarity = np.array([1])
pd_texts['類似度'] = np.concatenate([self_similarity, similarity[0]])
pd_texts.sort_values("類似度", ascending=False)



