import unittest
from Minimax.minimax import MinimaxNode, Board

class TestMinimaxNode(unittest.TestCase):
    def test_generate_children(self):
        b = Board()
        node = MinimaxNode(b, Board.PLAYER1)
        node.generateChildren()
        for p in range(9):
            with self.subTest(p=p):
                gb = [' '] * 9
                gb[p] = Board.PLAYER1_SYMBOL
                self.assertEquals(node.children[p].gameBoard.gameBoard, gb)