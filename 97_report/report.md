#応用情報工学演習（谷口研）レポート

* 学籍番号　　：4617054
* 氏名　　　　：鳥羽　望海
* グループ番号：３
* メンバー　　：鎌田　大己，鳥羽　望海，藤原　尚志

## 1. 作成したプログラムの概要，工夫点

1対1で通信対戦できる，ジェスチャーで操作するテトリスを作成した．工夫点としては，次の3点が挙げられる．

* ジェスチャー部分では前に撮影された画像に映った掌の座標との差分値を取り，その値によってテトリミノが移動するようにした
* Herokuを使用することによって，オンラインで通信対戦できるようにした
* 講義で作成したマインスイーパーでは実現されていなかったPyQtの軽量化を行なうことによって，テトリスをスムーズに動作させるようにした

 ## 2. 自身の役割，担当機能の説明，工夫点，苦労したことなど

自身の役割，担当機能の説明，工夫点，苦労したことなど

以下の7つを自身の役割として挙げ，それぞれに関して工夫した点や苦労したことなどを説明する．

1. テトリス，ジェスチャー，通信を組み合わせるアイディアの創出

   これに関してはグループ全体で考えた．以下の3点を踏まえ，演習に取り組んだ．

   * Pythonで利用可能なサードパーティーのGUI作成ライブラリーであり，演習でも利用した`PyQt`を利用してプログラムを作成する
   * 近年，社会的に最も利用価値の高い情報技術のうちの1つともなっているマシーンラーニングおよびAIを利用してプログラムを作成する
   * 娯楽的でありながら将来的な実用的発展を想起させる新規性の高いプロジェクトにする

2. 役割分担，クラス図の作成

   大きな役割として「ジェスチャーの作成」「テトリスの作成」「サーバー・クライアントの作成」の3つに分担し，それぞれ鳥羽，藤原，鎌田の３人が役割を担うことにした．

3. テトリスをジェスチャーで動かすためのプログラムの改修・作成

   ウェブ上にアップロードされていた[AirGesture](https://github.com/uvipen/AirGesture)を改修する形式で掌や拳の認証をすることにした．発表日時までが1ヶ月と短いことから，このように既存のジェスチャーモデルを利用したことは妥当だと考えられる．

   工夫した点としては，AirGestureでは画像の中にある掌や拳の座標値を取りその値を直接利用する形式だったが，差分を取る形式に変更した点が挙げられる．具体的に説明する．まず，ある画像1を取得しその画像に映っている掌や拳の座標値を取得する．次に，掌や拳が移動した後の画像2を取得しその画像についても同様に座標値を取得する．最後に，画像1と2に対応する座標値の差分を取得し，掌の状態になっている場合，デカルト座標系において$x-axis$方向に正の値を取っていればテトリミノを右に，負の値ならば左に，$y-axis$方向に負の値を取っていれば下に，拳の状態になっている場合は右回転し，他の場合は何もしない，というふうにした．

   苦労した点としては，ジェスチャー認証にはウェブ上に様々なものがアップロードされていたりAPIが提供されていたりしたが，有用なものを発見するまでに1週間近くかかった点である．最終的に，Googleにより開発された機械学習用ソフトウェアライブラリであるTensorFlowを利用していたAirGestureとなった．

   以下の部分でジェスチャーの差分を取っている（`src/gesture/core.py`）

   ```python
           while cv2.waitKey(10) != ord('q'):
   
               frame = self.cap.read()[1]
               frame = cv2.flip(frame, 1)
               frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               boxes, scores, classes = self.detect_hands(frame)
               results = self.predict(boxes, scores, classes)
   
               if len(results) == 1:
                   x, y, category = results[0]
                   # category 2 is Closed hand
                   if category == 2:
                       text = 'f'
                   # elif abs(x-_x) < eps and abs(y-_y) < eps_down:
                   #     text = ''
                   elif x - _x > eps:
                       text = 'l'
                   elif _x - x > eps:
                       text = 'h'
                   elif y > down_thres:
                       text = 'k'
                   else:
                       continue
   
                   _x, _y = x, y
   
               else:
                   x, y = _x, _y
                   continue
   ```

   また，TensorFlowのモデルは以下の部分で読み込んでいる（同上）

   ```python
   class Gesture(object):
   
   
       def __init__(self, builtin: bool=True):
   
           self.builtin = builtin
   
           tf.flags.DEFINE_integer('width', 640, 'Screen width')
           tf.flags.DEFINE_integer('height', 480, 'Screen height')
           tf.flags.DEFINE_float  ('threshold', 0.6, 'Threshold for score')
           tf.flags.DEFINE_float  ('alpha', 0.3, 'Transparent level')
           self.FLAGS = tf.flags.FLAGS
   
           model_path = '../gesture/model.pb'
           self.load_graph(model_path)
           self.capture()
   ```

4. テトリスのアルゴリズムをPythonへ移植・作成

   テトリスのアルゴリズムをウェブ上にあるそのアルゴリズムを説明してくれているサイトを参考にPythonでゼロから構築した．

   工夫した点としては，NumPyなど，サードパーティー系のライブラリーを利用せず，ネイティブなPythonで作成したことが挙げられる．これによって，将来的なテトリスのPythonによるアルゴリズムの移植を考えた場合のサードパーティーを利用できない場合（インターネットに接続していない状態のRaspberry Piなど）に対処できる．

   苦労した点として，最初はウェブ上にアップロードされている既存のPython版テトリスのアルゴリズムを利用しようとし複数のプログラムを実行してみたが，これらは全て適切な動作をしないことが判明し，後に[テトリスアルゴリズム（バンブーサテライツによる）](http://www.bamboo-satellites.com/as/tetris/)を参考にし，ゼロからPython版テトリスのアルゴリズムを構築することにした．テトリスのアルゴリズムをPythonで構築するための備忘録として鳥羽は[独自にウェブサイトにまとめた](https://withcation.com/2019/12/03/pythonでtetrisアルゴリズムを考える-1/)．

   以下の部分は独自に宣言した`Board`と`Tetrimino`の2つのクラスである（`src/alg/Tetris.py`）

   ```python
   class Board(object):
   
       def __init__(self, board_size: [int]):
   
           if type(board_size) is not list or len(board_size) != 2:
               raise TetrisError(f'board_size must be list and its length is just 2.<board_size={board_size}>')
   
           self.board = [[0 for _ in range(board_size[1])] for _ in range(board_size[0])]
   
   
       def __getitem__(self, key: int or tuple):
   
           if type(key) is int:
               return self.board[key]
           elif type(key) is tuple and len(key) == 2:
               return self.board[key[0]][key[1]]
           else:
               raise TetrisError(f'Irregal key.<key={key}>')
   
   
       def __setitem__(self, key: int or tuple, val2: int or [int]):
   
           if type(key) is int:
               if type(val2) is int:
                   for i in range(len(self.board[key])):
                       self.board[key][i] = val2
               elif type(val2) is list:
                   for i in range(len(self.board[key])):
                       self.board[key][i] = val2[i]
               else:
                   raise TetrisError(f'Irregal value.<val2={val2}>')
           elif type(key) is tuple and len(key) == 2 and type(val2) is int:
               self.board[key[0]][key[1]] = val2
           else:
               raise TetrisError(f'Irregal key.<key={key}>')
   
   
       def __repr__(self):
   
           res = ''
           for part in self.board:
               for element in part:
                   res += f'{element} '
               res = f'{res[:-1]}\n'
   
           return res[:-1]
   
   
       def list2board(self):
           print('YES')
           pass
   
   
   
   def list2board(board_li: list) -> Board:
   
       size = [20, 10]
       board = Board(size)
       for i in range(size[0]):
           for j in range(size[1]):
               board[i][j] = board_li[i][j]
   
       return board
   
   
   
   # 本当は構造体にしたいけど，Pythonにはないから
   class Tetrimino(object):
   
       def __init__(self):
   
           self.t4mino_li = [
               # i
               [[[1, i] for i in range(4)],
                [[i, 1] for i in range(4)]] * 2,
               # o
               [[[0, 0], [0, 1], [1, 0], [1, 1]]] * 4,
               # t
               [[[0, 1]] + [[1, i] for i in range(3)],
                [[1, 2]] + [[i, 1] for i in range(3)],
                [[2, 1]] + [[1, i] for i in range(3)],
                [[1, 0]] + [[i, 1] for i in range(3)]],
               # j
               [[[0, 0]] + [[1, i] for i in range(3)],
                [[0, 2]] + [[i, 1] for i in range(3)],
                [[2, 2]] + [[1, i] for i in range(3)],
                [[2, 0]] + [[i, 1] for i in range(3)]],
               # l
               [[[0, 2]] + [[1, i] for i in range(3)],
                [[2, 2]] + [[i, 1] for i in range(3)],
                [[2, 0]] + [[1, i] for i in range(3)],
                [[0, 0]] + [[i, 1] for i in range(3)]],
               # s
               [[[0, 1], [0, 2], [1, 0], [1, 1]],
                [[0, 0], [1, 0], [1, 1], [2, 1]]] * 2,
               # t
               [[[0, 0], [0, 1], [1, 1], [1, 2]],
                [[0, 1], [1, 0], [1, 1], [2, 0]]] * 2
           ]
   
   
       def __getitem__(self, key: tuple):
   
           if type(key) is not tuple or len(key) != 2:
               raise TetrisError(f'Irregal key.<key={key}>')
   
           return self.t4mino_li[key[0]][key[1]]
   ```

5. PyQt内におけるQFrameを用いたGUIの軽量化

   マインスイーパーではその特性上，セルをボタンにより実現されていたが，テトリスではPyQt内で要求されるCSSの不安定さを鑑みて，QPushButtonの代わりにQFrameを利用した．これにより，描画の高速化および軽量化を実現することに成功した．

   苦労した点としては，CSSがテトリスの描画に影響していたという事実に気付くのに時間がかかったということである．

   はじめはPython内でAbortion Trapが発生した際，NumPyに起因するものだと推測した．というのはNumPyの内部はC言語やFORTRANにより実装されており，アドレス割当に関する問題が励起したのではないかと考えたためである．そこでテトリスアルゴリズム内において，生のポインターを利用することができないようにNumPyから独立した独自のクラス`Board`を宣言することにした．しかしながら，これによる解決は望めなかった．

   次に考えたのがCSSの不安定さだった．しかしこれはプログラムを数百行書き換える必要があると判明した．結果的に描画を安定させるためにはCSSを利用しないように，つまりQPushButtonやQLabelによる実現は不可能でありその部分を軽量化するためにプログラムを書き換える以外ないということで，マインスイーパーにおけるQPushButtonに関する部分をQFrameに書き換えることにした．

   以下が軽量化した例のクラス`MyFrame`である（`src/gui/main.py`）

   ```python
   class MyFrame(QFrame):
   
       def __init__(self, board_size: [int]):
   
           super().__init__()
   
           self.color_dic = [
               0x808080,   # nothing, space
               0x00ffff,   # i, cyan
               0xffff00,   # o, yellow
               0xff00ff,   # t, purple
               0x0000ff,   # j, blue
               0xff8000,   # l, orange
               0x00ff00,   # s, green
               0xff0000    # t, red
           ]
           self.board_size = board_size
           self.part_board = Board(self.board_size)
           self.to = Tetrimino()
   
   
       def paintEvent(self, event):
   
           rect = self.contentsRect()
   
           for i in range(self.board_size[0]):
               for j in range(self.board_size[1]):
                   self.draw_square(i, j)
   
           self.update()
   
   
       def draw_square(self, i: int, j: int):
   
           rect_h = self.contentsRect().height() / self.board_size[0]
           rect_w = self.contentsRect().width() / self.board_size[1]
   
           painter = QPainter(self)
   
           color = QColor(self.color_dic[self.part_board[i, j]])
           i *= rect_h
           j *= rect_w
           painter.fillRect(j+1, i+1, j+rect_w-2, i+rect_h-2, color)
   
           painter.setPen(color.lighter())
           painter.drawLine(j, i+rect_h-1, j, i)
           painter.drawLine(j, i, j+rect_w-2, i)
   
           painter.setPen(color.darker())
           painter.drawLine(j+1, i+rect_h-1, j+rect_w-1, i+rect_h-1)
           painter.drawLine(j+rect_w-1, i+rect_h-1, j+rect_w-1, i+1)
   
   
       def update_board(self, fn):
   
           for i in range(self.board_size[0]):
               for j in range(self.board_size[1]):
                   self.part_board[i, j] = fn(i, j)
   
           self.update()
   
   
       def update_next(self, next_cur: int):
   
           t4mino = self.to.t4mino_li[next_cur][0]
           for i in range(self.board_size[0]):
               for j in range(self.board_size[1]):
                   self.part_board[i, j] = next_cur + 1 if [i, j] in t4mino else 0
   
           self.update()
   ```

   

6. 罰ゲームとして出力される顔写真の認証・ブロードキャスト演算位関するプログラムの作成

   罰ゲームとして積んだテトリス．具体的には，次の動作を行なう．

   1. ゲームが始まる前にHaar Cascadesを利用した方式で顔を認証し撮影する．撮影できない場合はゲームを始められないようにする
   2. テトリスのゲームを行なう
   3. ゲームで勝った場合は「You Win」の表示を行なう．負けた場合は「You Lose」の表示と同時に，積んだのテトリミノのブロック分だけ晒された顔画像を出力する

   工夫した点としては，NumPyで提供されているブロードキャスト演算およびrepeatによる行列の拡張を用いることで，円滑に罰ゲーム画像を計算できるようにした点である．

   苦労した点としては，最初はこれをQMessageBoxにより実現しようと考えていたが，これはOS Xにおいて画像を出力できないという問題があることが判明し別の方式を考える必要が発生したということが挙げられる．この対策として，実際のテトリスのゲームを行なったウィンドウとは異なったサブウィンドウを生成し，そこに画像を掲載することにした．これにより，罰ゲームを実現できた．

   悔いが残った点としては，負けた画像をTwitterなどのSNSを経由して送信するような実装をしたかったができなかったということである．他のプログラムのバグ等を取り除くことに時間を取られてしまい，Twitterにより提供されるAPI部分を実装できなかった．

   最初の顔認証部分は以下のようになっている（`src/gui/main.py`）

   ```python
       def set_loser_image(self, skip=False):
   
           loser_size_tup = (320, 640)
   
           cap = cv2.VideoCapture(0)
           detector = ObjDetector('haarcascade_frontalface_default.xml')
           while True:
               frame = cap.read()[1]
               height = frame.shape[0]
               width = height // 2
               frame = frame[:, frame.shape[1]//2-width//2:frame.shape[1]//2+width//2]
               if skip:
                   break
               if detector.detect(frame):
                   print('あなたの顔を人質に取ったよ！　ばら撒かれたくなかったら，TETRISで勝ってね！')
                   break
               sleep(0.2)
               print('おいちょっと面貸せや〜')
   
           self.loser_img = cv2.resize(frame, loser_size_tup)
   
           cap.release()
   ```

   ブロードキャスト演算は以下の部分で行なっている（同上）

   ```python
       def get_loser_image(self) -> np.ndarray:
   
           g = self.game
           frame = self.loser_img
           loser_size_tup = (320, 640)
   
           board_np = np.array(g.board.board)
           repeater = loser_size_tup[1] // board_np.shape[0]
           filt = board_np.repeat(repeater, axis=0).repeat(repeater, axis=1)
           filt[filt >= 1] = 1
           loser_img = np.zeros_like(frame)
           for ix in range(3):
               loser_img[..., ix] = frame[..., ix] * filt
   
           return loser_img
   ```

7. 発表するためのパワーポイントのプロットの作成

   最後の発表の際にパワーポイントを作成することになったが，分担的な作業を3人で行なっていたため，どのようにパワーポイントを書くか共通の規格がなかったため行なった．結果的にシンプルで分かりやすいパワーポイントを作成することができたと考えられる．

## 3. 感想

まず，応用情報工学演習全体についての感想を述べる．私はPythonを書くのに少しばかりの自信があったが，PyQtやOpenCVにおけるカスケード分類器の利用方法など私の知らない部分のPythonが多くあり，学べる部分がたくさんあった．演習全体を通して，知らないことをGoogleで検索したり，Qiitaの記事を読むことで，検索力を向上させることができたと自負している．

また，この演習期間にPython3.8.0がリリースされたことにより，新しいもの好きの私はついインストールをしてしまったため，TensorFlowやOpenCVなどのサードパーティー製ライブラリー，さらにはAnaconda NavigatorなどのIDEを動作させなくしてしまったことがあった．加えて，演習では利用していなかったが，MacのOS XをMojaveからCatalinaに更新させてしまったためにPydubやTkInterなどを動作させないようにしてしまい，その影響を被り他のライブラリーを探さなければならないという時間の浪費をすることになってしまった．結果的にはこの演習で培った検索力で，別のライブラリーをインストールする，`sys.path.append`によりAnacondaにインストールしたライブラリーを召喚するなどの回避策を使えたため，それほどの問題は発生しなかったが，今回の反省を踏まえて，新しいものがアップロードされていても，すぐに更新しないように心がけたいと考えた．

次に，今回のグループによる発表に関して述べる．私の希望通りのグループ編成となり，プログラムを組むのが得意な2人と共にプロジェクトを進められたため，GitHubの利用，サードパーティー製ライブラリーの共有，サーバーの利用などがスムーズに行なえた点は，非常に良いと考えられた．大学に入ってから大学内においてこのような経験ができたのはおそらくこれが初めてだったため，切磋琢磨しプログラムを組めたと自負している．

最後に，他グループの発表に関して述べる．様々なグループがWeb APIを利用したものや顔認証，画像認証を利用したものを作成しており，ビジュアルに訴えるソフトウェア開発が重要だと考えた．というのは，私たちが開発したものは決して技術では劣っていないはずでもビジュアルに訴える点で劣っているのではないかと考えたからだ．やはりプログラムを組む上で，UI/UXというのは重要だと考え，もし私たちがそれを自身のプロジェクトに組み込むならば，ジェスチャー認証の部分でインカメラで撮影した映像も映し出すべきだったのではないかと考えられる．

## 参考文献

* [AirGesture](https://github.com/uvipen/AirGesture)

* [テトリスアルゴリズム（バンブーサテライツによる）](http://www.bamboo-satellites.com/as/tetris/)

## 提出するプログラムに関して

以下のGitHubのページにプログラムを掲載する．

[wakame-tech/vendredi-noir GitHub](https://github.com/wakame-tech/vendredi-noir)

プログラムの利用方法を以下に記載する

* ターミナル上で`git clone https://github.com/wakame-tech/vendredi-noir`を実行
* 実行プログラムのあるディレクトリー`vendredi-noir/src/gui/`へ移動
* `python main.py`を実行．ただし，実行可能な形式として，Python3.7.xのみと規定した．それ以外のバージョンでは動作が保証されないため，実行を強制的に禁止としている．

### 注意

* `src/alg/Tetris.py`は将来性を考えてネイティブなPythonで書かれているため，特にpipをする必要はありませんが，サードパーティー製ライブラリーがインストールされていない場合，実行できない可能性があります．例えばPython-SocketIO，TensorFlow，PyQt5，Python-OpenCV2，NumPyなどです．
* プロジェクトで動作確認として利用したPCはMacBook Air 2017年モデルmacOS Catalinaです．それ以外のPCでは動作不良が起こる虞があります．
