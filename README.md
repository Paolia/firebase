# FirebaseとRaspberry Piを利用した監視カメラ
## 概要
Firebaseのデータベースの利点として、データベースに変更があると、
接続しているクライアントにその情報がプッシュされるということがあります。
それを利用して監視カメラを作成してみました。

## 構成
### Raspberry Pi
Raspberry Pi 3B
マイクロ波センサ（モーションセンサ）
WEBカメラ
Pythonプログラム

### PC側
HTML：講義で製作したものの改造版

### Firebase
Firestore Database 撮影の通知に使用
Storage 撮影した画像データをアップロード

## 処理内容
### Raspberry Pi側
Pythonのプログラムで一般的なwhile分の無限ループ（+エラーハンドラ）を回し、
その中の条件節でセンサの接続されているピンを監視している。
ピンに入力があると画像処理ライブラリで撮影し、そのデータをStorageに
アップロードしている。並行して、Firestore Databaseに通知を送信。

### PC側
HTMLは単純にFirestore Databaseの変更を監視し、変更があればその内容を表示する。

## 苦しんだ点・課題点
Firebaseの公式ドキュメントがわからん！そのおかげで数日溶かしてしまいました。
QiitaとかNoteの方がよっぽど役に立つ！それと、やっぱりPythonいいよPython!
