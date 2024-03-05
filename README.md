# python-analyzer
Pythonプロジェクトのimport関係を可視化するツール<br>
可視化にはgraphvizを使っています。
## 要求
graphviz, networkx
```sh
$ pip install -r requirements.txt
```
## 実行方法
```sh
$ analyzer.py ${analyze_dir}
```
outディレクトリに有向グラフが出力される。
