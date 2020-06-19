import multiprocessing


bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count()

accesslog = '-'
errorlog = '-'
loglevel = 'info'

# 開発時には、preload_appをFalseにし、reloadをTrueとする
reload = False
# コード直下に書かれたモデル読み込みなどを実行した後に、プロセスをフォークする
preload_app = True
