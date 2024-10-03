#from fastapi import FastAPI, HTTPException
#import datetime
#from model import get_data_from_firestore

import firebase_admin
from firebase_admin import credentials, firestore

try:
    #firebase_admin.initialize_app()
    cred = credentials.Certificate('/Users/takahiroinaba/src/github/tinaba96/uniqueness/firestore.json')
    firebase_admin.initialize_app(cred)

    db = firestore.client()
    #users_ref = db.collection(u'test')
    datas = db.collection(u'ai-analysis')
    docs = datas.get()

    print('start')
    print(docs)
    for doc in docs:
        print(f'Document ID: {doc.id}')
        data = doc.to_dict()  # フィールドの値を辞書形式で取得

        # フィールドごとの値を出力
        for field, value in data.items():
            print(f'{field}: {value}')


except Exception as e:
    print('error')
    print(e)

