import unittest
import Minesweeper as ms
import importlib
importlib.reload(ms)

class TestMinesweeper(unittest.TestCase):
    
    def test_init_game_board(self):
        """ ゲーム盤の初期化 """
        b = ms.Game()
        
        # セルのサイズは8x8
        nrows = len(b.game_board)
        ncols = len(b.game_board[0])
        self.assertEqual(ms.MS_SIZE, nrows)
        self.assertEqual(ms.MS_SIZE, ncols)
        
        # すべてのセルがCLOSE状態
        self.assertEqual(ms.CLOSE, b.game_board[0][0])
        self.assertEqual(ms.CLOSE, b.game_board[7][7])

    def test_init_mine_map(self):
        """ 地雷マップの初期化 """
        def count_mines(minemap):
            """ """
            count = 0
            for y in range(ms.MS_SIZE):
                for x in range(ms.MS_SIZE):
                    if minemap[y][x] < 0:
                        count = count + 1
            return count

        """ 指定した地雷数で初期化できるかチェック """
        b = ms.Game()
        b.init_mine_map(10)
        self.assertEqual(10, count_mines(b.mine_map))
        b.init_mine_map(3)
        self.assertEqual(3, count_mines(b.mine_map))
        b.init_mine_map(-1)
        self.assertEqual(0, count_mines(b.mine_map))
        b.init_mine_map(ms.MS_SIZE*ms.MS_SIZE)
        self.assertEqual(ms.MS_SIZE*ms.MS_SIZE, count_mines(b.mine_map))
        b.init_mine_map(ms.MS_SIZE*ms.MS_SIZE+1)
        self.assertEqual(ms.MS_SIZE*ms.MS_SIZE, count_mines(b.mine_map))
        
    def test_count_mines(self):
        """ 地雷数のカウント"""
        b = ms.Game()
        b.mine_map = [[0, 0, 0, 0, 0, 0, 0, -1],
                      [0,-1, -1, 0, 0, 0, 0, -1],
                      [0,-1, -1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, -1]]
        
        b.count_mines()
        self.assertEqual(1, b.mine_map[0][0])
        self.assertEqual(2, b.mine_map[0][1])
        self.assertEqual(2, b.mine_map[0][2])
        self.assertEqual(1, b.mine_map[0][3])
        self.assertEqual(2, b.mine_map[0][6])
        self.assertEqual(-1, b.mine_map[0][7])  # 地雷セルは-1のまま
        self.assertEqual(-1, b.mine_map[1][1])  # 地雷セルは-1のまま
        self.assertEqual(0, b.mine_map[5][5])   # 地雷が近傍にないセルは0のまま   

    def test_init(self):
        """ 初期化メソッドのテスト """
        b = ms.Game()
        nrows = len(b.mine_map)
        ncols = len(b.mine_map[0])
        self.assertEqual(ms.MS_SIZE, nrows)
        self.assertEqual(ms.MS_SIZE, ncols)
        nrows = len(b.game_board)
        ncols = len(b.game_board[0])
        		
    def test_open_cell(self):
        """ open_cellメソッドのテスト """
        b = ms.Game()
        
        b.mine_map = [[1, 2, 2, 1, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 1, 1], 
                      [1, 2, 2, 1, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1],
                      [0, 0, 0, 0, 0, 0, 1, -1]]
        b.game_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]]
        
        # すべての近傍セルを開き，Trueを返す
        self.assertEqual(True, b.open_cell(1,5))
        self.assertEqual(1, b.game_board[4][0])
        self.assertEqual(1, b.game_board[4][1])
        self.assertEqual(1, b.game_board[4][2])
        self.assertEqual(1, b.game_board[5][0])
        self.assertEqual(1, b.game_board[5][1])
        self.assertEqual(1, b.game_board[5][2])
        self.assertEqual(1, b.game_board[6][0])
        self.assertEqual(1, b.game_board[6][1])
        self.assertEqual(1, b.game_board[6][2])
        
        # 地雷セルを開けたらFalseを返す
        self.assertEqual(False, b.open_cell(1, 1))
        
        # 地雷セルが8近傍に含まれていた場合
        b.game_board[6][7] = 2
        self.assertEqual(True, b.open_cell(6, 6))
        self.assertEqual(1, b.game_board[6][6])
        self.assertEqual(2, b.game_board[6][7]) # FLAGが設定されたセルは変更なし
        self.assertEqual(1, b.game_board[7][6])
        self.assertEqual(0, b.game_board[7][7]) # 地雷セルは開かない
        
        # FLAGが設定されたセルを開いた場合
        b.game_board[6][7] = 2
        self.assertEqual(True, b.open_cell(7, 6))
        self.assertEqual(1, b.game_board[6][7]) # FLAGが設定されたセルを開く 

        # 既に開いているセルを開いた場合，近傍セルを開かない
        self.assertEqual(1, b.game_board[4][1])
        self.assertEqual(True, b.open_cell(1, 4))
        self.assertEqual(0, b.game_board[3][1])
        self.assertEqual(0, b.game_board[3][0])
        self.assertEqual(0, b.game_board[3][2])
        self.assertEqual(1, b.game_board[4][0]) # OPEN(1)のまま
        self.assertEqual(1, b.game_board[4][1]) # OPEN(1)のまま
        self.assertEqual(1, b.game_board[4][2]) # OPEN(1)のまま
        self.assertEqual(1, b.game_board[5][0]) # OPEN(1)のまま
        self.assertEqual(1, b.game_board[5][1]) # OPEN(1)のまま
        self.assertEqual(1, b.game_board[5][2]) # OPEN(1)のまま
        
        # ゲーム盤の縁で正しく動作するか?
        self.assertEqual(True, b.open_cell(0, 0))
        self.assertEqual(1, b.game_board[0][0])
        self.assertEqual(1, b.game_board[0][1])
        self.assertEqual(1, b.game_board[1][0])
        self.assertEqual(0, b.game_board[-1][0])  # -1の扱い
        self.assertEqual(0, b.game_board[0][-1])
    
    def test_flag_cell(self):
        """ flag_cellメソッドのテスト"""
        b = ms.Game()
        b.mine_map = [[1, 2, 2, 1, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 1, 1], 
                      [1, 2, 2, 1, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1],
                      [0, 0, 0, 0, 0, 0, 1, -1]]
        b.game_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]] 
        
        # CLOSE状態のセルにFLAGを設定
        b.flag_cell(0, 0)
        self.assertEqual(2, b.game_board[0][0])  # 0 --> 2
        self.assertEqual(0, b.game_board[0][1])
        
        # FLAG状態だったらCLOSE状態に戻す
        b.game_board[0][0] = 2
        b.flag_cell(0, 0)
        self.assertEqual(0, b.game_board[0][0])  # 2 --> 0
        
        # OPEN状態のセルにはFLAGを設定しない
        b.game_board[0][0] = 1
        b.flag_cell(0, 0)
        self.assertEqual(1, b.game_board[0][0])  # 1 --> 1
    
    def test_is_finished(self):
        """ ゲームが終了したか（すべてのセルを開けたか）チェック """
        b = ms.Game()
        b.mine_map = [[1, 2, 2, 1, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 2, -1], 
                      [2, -1, -1, 2, 0, 0, 1, 1], 
                      [1, 2, 2, 1, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1],
                      [0, 0, 0, 0, 0, 0, 1, -1]]
        b.game_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0]] 
        
        # すべてのセルがCLOSE状態であればFalse
        self.assertEqual(False, b.is_finished())
        
        # 地雷以外のセルをすべてOPEN状態にするとTrueを返す
        for y in range(ms.MS_SIZE):
            for x in range(ms.MS_SIZE):
                if b.mine_map[y][x] != -1:
                    b.game_board[y][x] = ms.OPEN
        self.assertEqual(True, b.is_finished())
        
        # 一つをCLOSE状態に変えるとFalseを返す
        b.game_board[0][0] = ms.CLOSE
        self.assertEqual(False, b.is_finished())

        # 地雷がないセルがFLAG状態だったらFalseを返す
        b.game_board[0][0] = ms.FLAG
        self.assertEqual(False, b.is_finished())
        
        # 地雷セルはFLAGでもOK(Trueを返す)
        b.game_board[0][0] = ms.OPEN
        b.game_board[1][1] = ms.FLAG
        self.assertEqual(True, b.is_finished())
        
        
if __name__ == '__main__': 
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)
