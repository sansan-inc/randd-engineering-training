# プロトタイプを作成する際の指南書

Linux 上で Python 言語を用いて機械学習を用いた Web アプリケーションもしくは WebAPI でプロトタイプを開発する際の方法を紹介します。

## サンプルコード概要

こちらのレポジトリの `samples/python_webapi` ディレクトリ以下をご確認ください。

scikit-learn で提供されている [Boston House Prises dataset](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_boston.html) について、回帰により「所有者が占有している家屋の$ 1000 単位の中央値」を求めます。

コードは大まかには、次の要素で構成されています。

* Dockerfile：コンテナ定義
* guniconf.py：WSGIサーバの設定
* setup.py, setup.cfg, requirements.txt：Pythonパッケージとしてインストール
* src/randd_sample
   * api.py：FlaskによるWebAPI
   * service.py：WebAPIとして提供するサービスの実装
   * schema：JSONSchema
   * model：簡単な回帰と学習の実装
* tests：pytest によるテスト

回帰の学習、モデル出力、モデルを利用したWebAPIを含めたコードです。
Docker化やpytest、setup.py化、jsonschema など様々な基本的技術が入っています。

写経したり、動かしたり、改造したりして理解を深めることができます。

## 技術選定

Docker + Python + gunicorn + Flask での開発方法を紹介します。

### それぞれの技術を用いる理由

* Docker: コンテナサービスであるため、別環境でモデルやアプリケーションが動かないということを防ぐことができる。
* Python: 機械学習ライブラリが豊富にあるため。また、WebAPIの構築も手軽なため。
* gunicorn: Python向けのWSGI HTTP Serverであり、プロセス起動後にワーカをフォークできるため、機械学習モデルを読んだ後にフォークという使い方ができる。
* Flask: Python 用の軽量なウェブアプリケーションフレームワークである。機能が必要最低限であるため、習得が容易である。

## モデルファイルの管理

GitLFS(Large File Storage)を使います。

## コーディングのお作法
* flake8
   * Pythonのスタイルガイドツール
* requirements.txt
   * バージョンを指定する

## その他参考資料

* [【Techの道も一歩から】第18回「アルゴリズムをコンテナ化しWebAPIとして利用可能に」](https://buildersbox.corp-sansan.com/entry/tech18_container)
* [【Techの道も一歩から】第20回「CircleCIとpytestに入門」](https://buildersbox.corp-sansan.com/entry/2019/06/10/114456)
* [【Techの道も一歩から】第21回「setup.pyを書いてpipでインストール可能にしよう」](https://buildersbox.corp-sansan.com/entry/2019/07/11/110000)
