from sudoku.cell import Cell
import sudoku.structure as structure

class State:
    cells = None
    steps = 0

    def __init__(self, cells):
        '''create an initial state from a cell array'''
        if cells is None or len(cells) != 81:
            raise RuntimeError("81 cells are required for a 9x9 sudoku")
        self.cells = cells
        self.propagateInitialValues()
        self.valid()


    def clone(self):
        '''return a deep clone of this state'''
        cells = [None]*81
        for i in range(81):
            cells[i] = self.cells[i].clone()
        clone = State(cells)
        clone.steps = self.steps
        clone.valid()
        return clone

    def getCells(self):
        '''return the array of all cells of this state'''
        return self.cells

    def setFinalCellVal(self, cell, val, ruleId):
        '''set the final value for a cell. Remove this value from all cells in all neighborhoods

           cell the cell, whose final value is known now
           val the final value
           ruleId the rule identifier, who discovered the final value
        '''
        self.steps += 1
        cell.setFinalVal(val, self.steps, ruleId)
        finalizedCellId = cell.getIdx()
        for n in structure.getNeighborHood(finalizedCellId):
            self.removeValueFromNeighborHood(val, finalizedCellId, n)
        self.valid()

    def valImpossibleInAtLeastOneNeighborhood(self, val, cell):
        '''take a value and search a neighborhood, in which this value is impossible for all its cells. If such a neighborhood is found,

        val the test value
        cell the cell, whose neighborhooda are checked
        return true, if a neighborhood is found, in which the value is impossible for all its cells; false, otherwise
        '''
        if val is None or not val in cell.getPossibleVals():
            raise RuntimeError(f'value invalid: {val}')
        idx = cell.getIdx()
        for n in structure.getNeighborHood(idx):
            if self.isValImpossibleInNeighborhood(val, idx, n):
                return True
        return False

    def getNumberFinalized(self):
        '''return the number of cells, whose value is known and this knowledge has been propagated to the cells neighborhoods'''
        finalized = 0
        for cell in self.cells:
            if cell.isFinalValueSet():
                finalized += 1
        return finalized

    def valid(self):
        '''check, whether this state is valid
           - the state is valid, if all neighborhoods are valid
           - a neighborhood is valid, if all finalized cells of it have different values
           If the state is not valid, throw an exception, otherwise return.
        '''
        for cell in self.cells:
            possibleVals = cell.getPossibleVals()
            if len(possibleVals) <= 0:
                raise RuntimeError('invalid cell: ' + cell.toString())
        for neighborHood in structure.getAllNeighborhoods():
            collect = set()
            for idx in neighborHood:
                cell = self.cells[idx]
                if cell.isOnlyOneValLeft():
                    finalVal = cell.getTheFinalVal()
                    if finalVal in collect:
                        raise RuntimeError(f'NeighborHood {",".join(map(str, neighborHood))} at idx {idx} has duplicate value {finalVal}')
                    collect.add(finalVal)

    def getSteps(self):
        '''return the number of steps, that have been done to solve the sudoku.
           By calling #setFinalCellVal(cell, val, char), the number of steps is incremented.
        '''
        return self.steps

    def incrSteps(self, attempts):
        '''increment the steps by the number of steps, that have been executed for a failing state copy
           (this occurs inside the 'backtrack' rule, if a temporary solution led to an inconsistent state).
           Should only be called by the 'backtrack' rule.
        '''
        self.steps = self.steps + attempts

    def toString(self):
        return self.toStringWithDetails(False)

    def toStringWithDetails(self, showDetails):
        '''create a readable representation, either compact or annotated by step number and rule (when the value was finalized)'''
        horizontalSeparator = None
        percentD = None
        empty = None
        if showDetails:
            stepLength = len(str(self.steps))
            stepLengthPlus5 = stepLength + 5
            horizontalCellHeader = " " + "-"*stepLengthPlus5
            horizontalLine = "+" + horizontalCellHeader*3 + " "
            horizontalSeparator = horizontalLine*3 + "+"
            percentD = "{:" + str(stepLength) + "d}"
            empty = " "*stepLengthPlus5
        else:
            horizontalSeparator = "+ - - - + - - - + - - - +"
            empty = " "
        sb = []
        first = True
        three = 0
        for i in range(81):
            if i % 9 == 0:
                if first:
                    first = False
                    sb.append(horizontalSeparator)
                    sb.append("\n| ")
                else:
                    sb.append("\n")
                    three += 1
                    if three == 3:
                        three = 0
                        sb.append(horizontalSeparator)
                        sb.append("\n| ")
                    else:
                        sb.append("| ")
            cell = self.cells[i]
            self.addCellInfo(sb, cell, showDetails, percentD, empty)
            if (i + 1) % 3 == 0:
                sb.append(" |")
                if (i + 1) % 9 != 0:
                    sb.append(" ")
            else:
                sb.append(" ")
        sb.append("\n")
        sb.append(horizontalSeparator)
        return "".join(sb)

    def propagateInitialValues(self):
        '''finalize the initialization of a state, after the initial values have been stored into the state.
           Propagate an initial value to the neighborhoods
        '''
        for cell in self.getCells():
            if cell.getRuleId() == 'I':
                initialCellId = cell.getIdx()
                val = cell.getTheFinalVal()
                for n in structure.getNeighborHood(initialCellId):
                    self.removeValueFromNeighborHood(val, initialCellId, n)

    def addCellInfo(self, sb, cell, showStep, percentD, empty):
        '''for a finalized cell, add the value and optional anotations:
           ruleId and step-number; otherwise add spaces.
        '''
        if cell.isFinalValueSet():
            sb.append(str(cell.getTheFinalVal()))
            if showStep:
                sb.append("(")
                sb.append(cell.getRuleId())
                sb.append(':')
                sb.append(percentD.format(cell.getStep()))
                sb.append(")")
        else:
            sb.append(empty)

    def isValImpossibleInNeighborhood(self, val, mineIdx, neighborHood):
        '''check for a single neighborhood, whether a value is impossible for all cells (except the one, that triggered the check)
           val the value to be checked
           mineIdx the index of the triggering cell; has to be excluded from the check
           neighborHood the cell id's of a neighborhood
           return true, if the value is impossible in the neighborhood
        '''
        for idx in neighborHood:
            if idx != mineIdx:
                cell = self.cells[idx]
                if cell.isValPossible(val):
                    return False
        return True

    def removeValueFromNeighborHood(self, finalVal, finalizedCellId, neighborHood):
        '''remove a value from the set of possible values of all cells of a neighborHood

           finalVal the value to be removed
           finalizedCellId the index of the cell, whose value was finalized; has to be excluded from the removal, of course
           neighborHood the cell id's of a neighborhood
        '''
        if len(neighborHood) != 9:
            raise RuntimeError(f'neighborhood is not of size 9: {",".join(neighborHood)}')
        for idx in neighborHood:
            if idx != finalizedCellId:
                self.cells[idx].removeFromSetOfPossibleValues(finalVal)