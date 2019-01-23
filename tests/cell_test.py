import unittest

from sudoku.cell import Cell
from sudoku.cell import idx2xy
from sudoku.cell import xy2idx

class CellTest(unittest.TestCase):

	def test_index(self):
		self.assertEqual(0, xy2idx(1, 1))
		self.assertEqual(8, xy2idx(9, 1))
		self.assertEqual(9, xy2idx(1, 2))
		self.assertEqual(80, xy2idx(9, 9))

		self.assertEqual([1, 1], idx2xy(0))
		self.assertEqual([9, 1], idx2xy(8))
		self.assertEqual([1, 2], idx2xy(9))
		self.assertEqual([9, 9], idx2xy(80))

	def  test_cell(self):
		c = Cell(10, [1, 3, 5])
		self.assertEqual(2, c.getX())
		self.assertEqual(2, c.getY())
		self.assertTrue(c.isValPossible(3))
		self.assertFalse(c.isValPossible(4))

	def  test_cell_setval(self):
		c = Cell(10, [1, 3, 4])
		c.setFinalVal(3, 0, '?')
		self.assertTrue(c.isValPossible(3))
		self.assertFalse(c.isValPossible(4))

	def  test_cell_setval_exc(self):
		c = Cell(10, [1, 3, 5])
		with self.assertRaises(RuntimeError): c.setFinalVal(2, 0, '?')

	def  test_cell_getval(self):
		fiveCell = Cell(0, [5])
		self.assertTrue(fiveCell.isOnlyOneValLeft())
		self.assertEqual(5, fiveCell.getTheFinalVal())
		fiveSixCell = Cell(0, [5, 6])
		self.assertFalse(fiveSixCell.isOnlyOneValLeft())

	def  test_cell_getval_exc(self):
		fiveSixCell = Cell(0, [5, 6])
		with self.assertRaises(RuntimeError): fiveSixCell.getTheFinalVal()
