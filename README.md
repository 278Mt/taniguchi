# taniguchi

## TL;DR

応用情報工学演習（谷口研）で利用、作成したプログラムについて書いてある

## 応用情報工学演習（谷口研）

東京理科大学工学部　情報工学科3年秋学期には必修として応用情報工学演習がある。

この科目は同学科に所属する研究室の中から2つ選び、演習を行なうものである。

このレポジトリーでは鳥羽が科目登録をしている谷口研究室に関するプログラム等を保存しておくことにしている。

## 行なったこと・このレポジトリーにあること

* Python3.xの基礎的な説明
* Jupyter NotebookによるPythonの利用
* PyQtの利用
* デバッガーの利用
* Minesweeperの作成（CUI、GUIともに）
* OpenCV-Pythonの利用
* Haarによる顔認識
* 講義資料（都合により削除することがある）

## 行なっていないこと・このレポジトリーにないこと

* Python3.xより前の実行プログラム
* 3人チームにより作成した最終課題（随時更新中）

## この講義についての所感

Pythonがある程度書ける前提で話が進むため、事前にPythonを勉強していない人にとってはやや酷。

最後の演習課題では3人1チームでプロジェクトとしてプログラムを作成する。

年度によって、ランダムにチームが組まれることや生徒たちの好み組まれることがある、らしい。

### この講義では……

次に列挙する内容に「？」とならなければ、だいたい講義についてゆける

* `list`のコピーは`a_li.copy()`のようにする必要がある
* `for`文は`for i in range(5):`のように宣言する
* `import numpy as np`と書いたことがある
* クラスを宣言するときは`class MyClass(object):`のように書く

逆に以下のことはあまり知らなくても平気

* `import cv2`や`import PyQt5`と書いたことがある
* Jupyter Notebookを使ったことがある
* ベンチマークテスト、イテレーターやジェネレーター、デコレーターを使ったことがある
* `def __add__(self):`と書けば`+`演算子を作成したクラス内でオーバーロードできる
* `map()`や`zip()`、`enumerate()`と書いたことがある