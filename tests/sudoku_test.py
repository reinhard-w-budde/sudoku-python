import unittest

import sudoku.do as do
import sudoku.rulemachine as rulemachine
import sudoku.runsudoku as runsudoku
from sudoku.state import State

class SudokuTest(unittest.TestCase):

	def testInit(self):
		with self.assertRaises(RuntimeError): State(None)
		with self.assertRaises(RuntimeError): do.string2cells("...")
		state = State(do.string2cells('.' * 81))
		self.assertIsNotNone(state)

	def testInitExampl3(self):
		state = State(do.string2cells(self.example(3)))
		state = rulemachine.ruleOneValLeft(0, state)

		for i in range(9):
			cell = state.getCells()[i]
			self.assertEquals(i + 1, cell.getTheFinalVal())
		for i in range(9, 27):
			cell = state.getCells()[i]
			self.assertEquals(6, len(cell.getPossibleVals()))
		for i in range(27, 81):
			cell = state.getCells()[i]
			self.assertEquals(8, len(cell.getPossibleVals()))

	def testClone(self):
		example2 = self.example(2)
		cells = do.string2cells(example2)
		state1 = State(cells)
		state2 = state1.clone()
		self.assertEquals(state1.toString(), state2.toString())
		self.assertEquals(state1.toStringWithDetails(True), state2.toStringWithDetails(True))

	def ignore_testOne(self):
		self.runTest(10)

	def testComplete(self):
		lastNumber = 11
		print(f'\nTESTING {lastNumber} SUDOKUS')
		for i in range(1, lastNumber):
			self.runTest(i)

	def runTest(self, number):
		print("\nNUMBER " + str(number))
		toSolve = self.example(number)
		solution = runsudoku.run(toSolve)
		expected = self.solution(number)
		if expected is not None:
			self.assertEquals(expected, solution.toString())

	def example(self, number):
		try:
			path = f'_examples/sudoku-{number:{0}{2}}'
			return runsudoku.readAllLines(path, "")
		except Exception:
			raise RuntimeError(f'File {path} could not be read')

	def solution(self, number):
		try:
			path = f'_solutions/sudoku-{number:{0}{2}}'
			return runsudoku.readAllLines(path, "\n")
		except Exception:
			return None
