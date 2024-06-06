#coding: utf-8
import RPi.GPIO as GPIO # GPIOライブラリのインポート。
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # BOARDモードに設定。左上からのピン番号でしてい。
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

import cv2 # OpenCVライブラリ。画像処理のため。
import os # 画像削除のため。
import pyrebase # 画像のStorageへのアップロードのため。参考例がこれだったので。
# pyrebaseはシンプルで使いやすそうだけど、DBがRealtime Databaseにしか対応していない。
# そちらの実装ライブラリ変更の余裕がなかったのでダサいけど、Cloud Firestore接続のため
# 別にfirebase_adminをインポート。

# ここからCloud Firestore接続準備。
import time 
import datetime
# import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
cred = credentials.Certificate("./test001-4e745-firebase-adminsdk-vsj0w-549db8d780.json")
# Cloud Firestore接続のためのクレデンシャル用リンク。
app = firebase_admin.initialize_app(cred)
db = firestore.client()
#today = datetime.datetime.fromtimestamp(time.time())
#date = today.strftime('%Y%m%d%H%M%S')
#data = {
#    'name':'RPi Detector',
#    'text':'誰かが来たよ！',
#    'time':date,
#}
# Cloud Firestore接続準備ここまで。

# こちらは画像を上げるStorage接続のため。
firebaseConfig = {
    'apiKey': "ひみつ",
    'authDomain': "ひみつ",
    'databaseURL': "ひみつ",
    'projectId': "ひみつ",
    'storageBucket': "ひみつ",
    'messagingSenderId': "ひみつ",
    'appId': "ひみつ",
  }
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

# Python定番のwhile Trueによる無限ループとtry/exceptによるエラーハンドラーによる
# イベントハンドラ。
while True:
    try:
        if GPIO.input(29) == GPIO.HIGH:
            # マイクロウエーブセンサーは基本HIGHかLOWしか出さないみたいなので、
            # 29番ピンで受けて判定する。
            print("動作検知！") # RPiローカルでメッセージを返す。
            now = datetime.datetime.now() # 現在時間をdatetime形式で取得。
            dt = now.strftime("%Y%m%d%H%M%S")
            # strftime関数でdatetimeを変換（○○○○年○○月○○日○○時○○分○○秒）
            name = dt+".jpg" # 取得した現在時刻から画像ファイル名を作成。
            cap = cv2.VideoCapture(0)
            
            # 画像撮影。このあたりの処理はOpenCVの処理なのでよくわかりません。
            ret, frame = cap.read()
            cv2.imwrite(name, frame)
            cap.release()
            cv2.destroyAllWindows()
            # img = cv2.imread(name)
            # cv2.imshow('image', img)
            # 撮影処理ここまで。
            
            print("撮影しました") # ローカルに撮影確認メッセージを表示。
            
            # ここでCloud Firebaseへデータを送信。現状では通知プッシュのためにしか使ってない。
            today = datetime.datetime.fromtimestamp(time.time())
            date = today.strftime('%Y%m%d%H%M%S')
            data = {
                'name':'RPi Detector',
                'text':'誰かが来たよ！',
                'time':date,
            }
            db.collection('environment').add(data)
            print(data)
            
            storage.child(name).put(name) # 画像をStorageの方へアップロード。
            print("Image sent to Firebase Storage.") # ローカルにアップロード確認メッセージを表示。
            #os.remove(name) # ローカルの画像削除処理。
            #print("File removed.") # ローカル画像削除のメッセージ。
            time.sleep(3) # -3秒待つ。
            
    except keyboardInterrupt:
        pass

GPIO.cleanup() # GPIOを開放。