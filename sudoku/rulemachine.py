import sudoku.do as do

RULE_ONE_VAL_LEFT = "RULE_ONE_VAL_LEFT"
RESULT_ONE_VAL_LEFT = "RESULT_ONE_VAL_LEFT"
RULE_EXCLUDED_VAL = "RULE_RULE_EXCLUDED_VAL"
RESULT_EXCLUDED_VAL = "RESULT_EXCLUDED_VAL"
RULE_BACKTRACK = "RULE_BACKTRACK"
RESULT_BACKTRACK = "RESULT_BACKTRACK"

def ruleOneValLeft(recDepth, state):
    """for for every cell C
       if: only one value is possible for C
       then: propagate this to C' neighborhood
       if: some cell could be finalized,
       then: call the rule recursively

       return the updated state, after the rule has finished
    """
    ruleOneValLeftId = 'O'
    do.logStartRule(RULE_ONE_VAL_LEFT, recDepth, ruleOneValLeftId, state)
    finalizedCellsBefore = state.getNumberFinalized()
    state = ruleOneValLeftSingleStep(recDepth, state)
    finalizedCellsAfter = state.getNumberFinalized()
    if finalizedCellsBefore != finalizedCellsAfter and finalizedCellsAfter < 81:
        state = ruleOneValLeft(recDepth + 1, state)
    do.logEndRule(RULE_ONE_VAL_LEFT, recDepth, ruleOneValLeftId, '', state)
    return state

def ruleOneValLeftSingleStep(recDepth, state):
    """for for every cell C
       if: only one value is possible for C
       then: propagate this to C' neighborhood
       return the updated state, after the rule has finished
    """
    ruleOneValLeftId = 'O'
    for cell in state.getCells():
        if not cell.isFinalValueSet() and cell.isOnlyOneValLeft():
            val = cell.getTheFinalVal()
            state.setFinalCellVal(cell, val, ruleOneValLeftId)
            do.logI(RESULT_ONE_VAL_LEFT, recDepth, f'{ruleOneValLeftId}: cell {cell.toXY()} = {val}')
    return state

def ruleExcludedVal(recDepth, state):
    """check for every cell C
       if: C's neighbarhood cannot hold a value V, which is possible for C
       then: V must be the correct value for C. Propagate this to C's neighbarhood if: some cell could be finalized,
       then: call the rule recursively

       return the updated state, after the rule has finished
    """
    ruleExcludedValId = 'E'
    do.logStartRule(RULE_EXCLUDED_VAL, recDepth, ruleExcludedValId, state)
    atLeastOneSuccess = False
    for cell in state.getCells():
        if not cell.isFinalValueSet():
            for val in cell.getPossibleVals():
                success = state.valImpossibleInAtLeastOneNeighborhood(val, cell)
                if success:
                    atLeastOneSuccess = True
                    state.setFinalCellVal(cell, val, ruleExcludedValId)
                    do.logI(RESULT_EXCLUDED_VAL, recDepth, f'{ruleExcludedValId}: cell {cell.toXY()} = {val}')
                    break
    state.valid()
    if atLeastOneSuccess and state.getNumberFinalized() < 81:
        state = ruleOneValLeft(recDepth + 1, state)
        state = ruleExcludedVal(recDepth + 1, state)
    do.logEndRule(RULE_EXCLUDED_VAL, recDepth, ruleExcludedValId, '', state)
    return state

def ruleBacktracker(recDepth, state, visitedCells):
    """check for every cell C, by stepping through all possible values V
       try: to solve the sudoko assumg that C's value is V
       success: done
       fail: backtrack to try the next possible value of C
       
       return the updated state, after the rule has finished
    """
    ruleBacktrackerId = 'B'
    do.logStartRule(RULE_BACKTRACK, recDepth, ruleBacktrackerId, state)
    while True:
        cell = pickCell(state, visitedCells)
        if cell is None:
            break
        idx = cell.getIdx()
        for val in cell.getPossibleVals():
            stateForTrial = state.clone()
            test = stateForTrial.getCells()[idx]
            try:
                do.logI(RESULT_BACKTRACK, recDepth, f'{ruleBacktrackerId}: TRY  cell {test} = {val}')
                stateForTrial.setFinalCellVal(test, val, ruleBacktrackerId)
                stateForTrial = ruleOneValLeft(recDepth + 1, stateForTrial)
                stateForTrial = ruleExcludedVal(recDepth + 1, stateForTrial)
                stateForTrial.valid()
                do.logI(RESULT_BACKTRACK, recDepth, f'{ruleBacktrackerId}: SUCC cell {test.toXY()} = {val}')
                if stateForTrial.getNumberFinalized() < 81:
                    stateForTrial = ruleBacktracker(recDepth + 1, stateForTrial, list(visitedCells))
                do.logEndRule(RULE_BACKTRACK, recDepth, ruleBacktrackerId, " FINAL SUCCESS", stateForTrial)
                return stateForTrial
            except RuntimeError:
                do.logI(RESULT_BACKTRACK, recDepth, f'{ruleBacktrackerId}: FAIL cell {cell} = {val}')
                state.incrSteps(stateForTrial.getSteps())
        do.logEndRule(RULE_BACKTRACK, recDepth, ruleBacktrackerId, f' NO SOLUTION for {cell.toXY()}', state)
        raise RuntimeError(f'{ruleBacktrackerId}: no solution (1)')
    do.logEndRule(RULE_BACKTRACK, recDepth, ruleBacktrackerId, f' NO SOLUTION AT ALL', state)
    raise RuntimeError(f'{ruleBacktrackerId}: no solution (2)')

def pickCell(state, visitedCells):
    """pick the cell with the least number of possible values, but only, if not already visited :-) and if not finalized"""
    minValsCell = None
    for cell in state.getCells():
        if not cell.getIdx() in visitedCells:
            if not cell.isFinalValueSet():
                minValsCell = cell
                break
    # all have been visited. Unsolvable sudoku (???)
    if minValsCell is None:
        return None
    # find the cell with the least number of possible values
    minValsSize = len(minValsCell.getPossibleVals())
    if minValsSize > 2:
        for cell in state.getCells():
            if not cell.getIdx() in visitedCells:
                if not cell.isFinalValueSet():
                    size = len(cell.getPossibleVals())
                    if size < minValsSize:
                        minValsSize = size
                        minValsCell = cell
                        if minValsSize <= 2:
                            break
    # mark it visited and return it
    visitedCells.append(minValsCell.getIdx())
    return minValsCell
