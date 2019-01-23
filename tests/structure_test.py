import unittest
import sudoku.structure as structure
from sudoku.cell import xy2idx

class structureTest(unittest.TestCase):
	def check(self, idx, hor, vert, block):
		neighbarhoods = structure.getNeighborHood(idx)
		self.assertEquals(hor, neighbarhoods[0])
		self.assertEquals(vert, neighbarhoods[1])
		self.assertEquals(block, neighbarhoods[2])

	def testNeighbarHood(self):
		self.check(0,  [0, 1, 2, 3, 4, 5, 6, 7, 8],
				       [0, 9, 18, 27, 36, 45, 54, 63, 72],
				       [0, 1, 2, 9, 10, 11, 18, 19, 20])
		self.check(40, [36, 37, 38, 39, 40, 41, 42, 43, 44],
				       [4, 13, 22, 31, 40, 49, 58, 67, 76],
				       [30, 31, 32, 39, 40, 41, 48, 49, 50])
		self.check(xy2idx(4, 1),
				       [0, 1, 2, 3, 4, 5, 6, 7, 8],
				       [3, 12, 21, 30, 39, 48, 57, 66, 75],
				       [3, 4, 5, 12, 13, 14, 21, 22, 23])

	def testIndex(self):
		self.assertEquals([1, 1], structure.xy2block(1, 1))
		self.assertEquals([1, 1], structure.xy2block(2, 1))
		self.assertEquals([1, 1], structure.xy2block(3, 1))
		self.assertEquals([1, 1], structure.xy2block(1, 3))
		self.assertEquals([1, 1], structure.xy2block(2, 2))

		self.assertEquals([7, 7], structure.xy2block(7, 7))
		self.assertEquals([7, 7], structure.xy2block(9, 9))
