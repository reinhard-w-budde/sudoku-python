class Cell:
    idx = 0
    possibleVals = []
    step = -1
    ruleId = '?'

    def __init__(self, idx, possibleVals):
        """create a new Cell with a set of possible values
           - idx the index of the Cell from 1...81
           - possibleVals set of possible values. Values are from 1...9
        """
        self.idx = idx
        self.possibleVals = list(possibleVals)

    def clone(self):
        """deep clone of this Cell"""
        cell = Cell(self.idx, list(self.possibleVals))
        cell.step = self.step
        cell.ruleId = self.ruleId
        return cell

    def getIdx(self):
        """get the index 1...81 of this Cell"""
        return self.idx

    def getX(self):
        """return the X index of the Cell (for pretty printing), starting from 1. Value is from 1...9"""
        return self.idx % 9 + 1

    def getY(self):
        """return the Y index of the Cell (for pretty printing), starting from 1. Value is from 1...9"""
        return self.idx // 9 + 1

    def setInitVal(self, val):
        """set the initial value. This is a value known from the beginning of the sudoku."""
        if val is None:
            raise RuntimeError("no value to set")
        self.possibleVals = [val]
        self.step = 0
        self.ruleId = 'I'

    def setFinalVal(self, val, step, ruleId):
        """set the final value for this Cell. If the value is NOT possible, an exception is thrown. This method should only be called by
           State#setFinalCellVal, which is responsible for propagating the finalization to the neighborhoods
           Note: see #isFinalValueSet() and #isOnlyOneValLeft()
        """
        if val is None:
            raise RuntimeError("invalid final value for a cell - logical error of a rule")
        if self.step >= 0:
            raise RuntimeError(f'Cell {self} got a final value for the second time - logical error of a rule')
        elif self.isValPossible(val):
            self.possibleVals = [val]
            self.step = step
            self.ruleId = ruleId
        else:
            raise RuntimeError(f'Cell {self} should be set to {val}, but that is impossible')

    def removeFromSetOfPossibleValues(self, val):
        """remove a value from the set of possible values. If the value was already removed, this is NO error"""
        try:
            self.possibleVals.remove(val)
        except ValueError:
            return None

    def getPossibleVals(self):
        """return the list of possible values"""
        return self.possibleVals

    def isValPossible(self, val):
        """is the given value possible?"""
        return val in self.possibleVals

    def isOnlyOneValLeft(self):
        """check if only one value is possible (i.e. the final value is known). This may have been propagated to the neighborhood or may not.
           Note: this method behaves similar to #isFinalValueSet()
        """
        return len(self.possibleVals) == 1

    def isFinalValueSet(self):
        """check if the final value has been set (explicitly) by calling #setFinalVal(Val, int, char)
           Note: if this method returns true, #isOnlyOneValLeft() will return true, too.
        """
        return self.step >= 0

    def getTheFinalVal(self):
        """return the final value of this Cell. If the final value is unknown, throw an exception"""
        size = len(self.possibleVals)
        if size != 1:
            raise RuntimeError(f'cell {self} has no final value, but is asked for that')
        for v in self.possibleVals:
            return v

    def getStep(self):
        """return the step, in which the final value was discovered. If the final value is unknown, return -1"""
        return self.step

    def getRuleId(self):
        """return the ruleId, that discovered the final value. If the final value is unknown, return '?'"""
        return self.ruleId

    def toXY(self):
        """return the x-y-coordinates of this Cell. X from left to right, starting with 1. Y from top to bottom, starting at 1"""
        return f'{{{self.getX()},{self.getY()}}}'

    def __str__(self):
        return f'{{{self.getX()},{self.getY()};[{",".join(str(e) for e in self.possibleVals)}]}}'

def idx2xy(idx):
    """convert an index to a x-y-coordinate of a Cell"""
    return [idx % 9 + 1, idx // 9 + 1]

def xy2idx(x, y):
    """convert a x-y-coordinate to the index of a Cell. Used for testing only"""
    return x + 9 * y - 10
