import re
from sudoku.cell import Cell

VALIDCHARS = re.compile('[123456789 .]{81,81}')
NOT_ENABLED = []
RUN = "RUN"

def string2cells(aS):
    """convert a string of length 81 to an Cell[81] array. Chars between '1' and '9'are considered already known cell values"""
    __check(aS)
    cells = [None] * 81
    for i in range(81):
        cells[i] = Cell(i, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    for i in range(81):
        charAtI = aS[i]
        if charAtI >= '1' and charAtI <= '9':
            cells[i].setInitVal(int(charAtI))
    return cells

def logStartRule(log, indent, ruleId, state):
    """log, that a rule started

       log logger to use
       indent depth of indentation
       ruleId name of rule to be started
       state of the solution
    """
    __logRule(log, indent, "++", ruleId, '', state)

def logEndRule(log, indent, ruleId, msg, state):
    """log, that a rule terminated

       log logger to use
       indent depth of indentation
       ruleId name of rule to be started
       state of the solution
    """
    __logRule(log, indent, "--", ruleId, msg, state)

def log(log, msg):
    """log a message"""
    if __isEnabled(log):
        print(msg)

def logI(log, depth, msg):
    """log a message with a indentation (for better reading)"""
    if __isEnabled(log):
        fmt = f'{log:{30}}: {". "*depth}{msg}'
        print(fmt)

def showState(state, showDetails):
    if __isEnabled(RUN):
        log(RUN, state.toStringWithDetails(showDetails))

def __check(aS):
    """check whether an input string might be a valid Sudoku definition:
       - 9 lines
       - each line 9 chars
       - each char 1...9 or '.' or ' '
    """
    if aS is None or len(aS) != 81:
        raise RuntimeError("invalid size. Must be 81")
    elif not VALIDCHARS.match(aS):
        raise RuntimeError("invalid chars. Must be 1..9 ' ' or '.'")

def __isEnabled(log):
    # return log == 'RUN'
    return not (log in NOT_ENABLED)

def __logRule(log, depth, prefix, ruleId, msg, state):
    """help to log that a rule started or finished"""
    if __isEnabled(log):
        fmt = f'{log:{30}}: {". "*depth}{prefix}{ruleId}: [{state.getNumberFinalized()}]{msg}'
        print(fmt)
