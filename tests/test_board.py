import unittest
from Minimax.minimax import Board

class TestBoardMethods(unittest.TestCase):
    def test_copy(self):
        b1 = Board()
        b2 = b1.copy()
        self.assertEqual(b1.gameBoard, b2.gameBoard)

    def test_move_registering(self):
        for p in range (9):
            with self.subTest(p=p):
                b1 = Board()
                b2 = Board()
                t_gb1 = b1.gameBoard.copy()
                t_gb2 = b2.gameBoard.copy()

                b1.registerMove(p, Board.PLAYER1)
                t_gb1[p] = Board.PLAYER1_SYMBOL
                
                self.assertEqual(b1.gameBoard, t_gb1)
                
                b2.registerMove(p, Board.PLAYER2)
                t_gb2[p] = Board.PLAYER2_SYMBOL

                self.assertEqual(b2.gameBoard, t_gb2)

    def test_evaluation_win(self):
        test_configs_p1 = [
            list(' {}  {}  {} '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('  {} {} {}  '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('{}{}{}      '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('{}   {}   {}'.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('   {}{}{}   '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('      {}{}{}'.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('{}  {}  {}  '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list(' {}  {}  {} '.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL)),
            list('  {}  {}  {}'.format(Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL, Board.PLAYER1_SYMBOL))   
        ]

        test_configs_p2 = [
            list(' {}  {}  {} '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('  {} {} {}  '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('{}{}{}      '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('{}   {}   {}'.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('   {}{}{}   '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('      {}{}{}'.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('{}  {}  {}  '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list(' {}  {}  {} '.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL)),
            list('  {}  {}  {}'.format(Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL, Board.PLAYER2_SYMBOL))   
        ]

        for config in test_configs_p1:
            with self.subTest(i1=len(test_configs_p1)):
                b = Board()
                b.gameBoard = config
                r = b.evaluateBoard(Board.PLAYER1)
                self.assertEquals(r, 1)

        for config in test_configs_p2:
            with self.subTest(i2=len(test_configs_p2)):
                b = Board()
                b.gameBoard = config
                r = b.evaluateBoard(Board.PLAYER2)
                self.assertEquals(r, 1)
