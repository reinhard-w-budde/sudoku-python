import unittest

import sudoku.do as do
import sudoku.rulemachine as rulemachine
import sudoku.runsudoku as runsudoku
from sudoku.state import State

class SudokuTest(unittest.TestCase):

	def test_init(self):
		with self.assertRaises(RuntimeError): State(None)
		with self.assertRaises(RuntimeError): do.string2cells("...")
		state = State(do.string2cells('.' * 81))
		self.assertIsNotNone(state)

	def test_initexample_3(self):
		state = State(do.string2cells(self.__example(3)))
		state = rulemachine.ruleOneValLeft(0, state)

		for i in range(9):
			cell = state.getCells()[i]
			self.assertEqual(i + 1, cell.getTheFinalVal())
		for i in range(9, 27):
			cell = state.getCells()[i]
			self.assertEqual(6, len(cell.getPossibleVals()))
		for i in range(27, 81):
			cell = state.getCells()[i]
			self.assertEqual(8, len(cell.getPossibleVals()))

	def test_clone(self):
		example2 = self.__example(2)
		cells = do.string2cells(example2)
		state1 = State(cells)
		state2 = state1.clone()
		self.assertEqual(str(state1), str(state2))
		self.assertEqual(state1.toStringWithDetails(True), state2.toStringWithDetails(True))

	@unittest.skip("enable to run a single test")
	def test_only_one_sudoku(self):
		self.__runTest(10)

	def test_all_example_sudokus(self):
		lastNumber = 11
		print(f'\nTESTING {lastNumber} SUDOKUS')
		for i in range(1, lastNumber):
			self.__runTest(i)

	def __runTest(self, number):
		print(f'\nNUMBER {number}')
		toSolve = self.__example(number)
		solution = runsudoku.run(toSolve)
		expected = self.__solution(number)
		if expected is not None:
			self.assertEqual(expected, str(solution))

	def __example(self, number):
		try:
			path = f'_examples/sudoku-{number:{0}{2}}'
			return runsudoku.readAllLines(path, "")
		except Exception:
			raise RuntimeError(f'File {path} could not be read')

	def __solution(self, number):
		try:
			path = f'_solutions/sudoku-{number:{0}{2}}'
			return runsudoku.readAllLines(path, "\n")
		except Exception:
			return None
