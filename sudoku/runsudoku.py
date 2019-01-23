from datetime import datetime
import sys

sys.path.append(".")

import sudoku.do as do
import sudoku.rulemachine as rulemachine
from sudoku.state import State

RUN = "RUN"

def run(aS):
    start = datetime.now()
    state = State(do.string2cells(aS));
    do.log(RUN, f'start with {state.getNumberFinalized()} known values')
    showState(state, False)
    state = rulemachine.ruleOneValLeftSingleStep(0, state)
    if state.getNumberFinalized() < 81:
        state = rulemachine.ruleExcludedVal(0, state)
        if state.getNumberFinalized() < 81:
            state = rulemachine.ruleBacktracker(0, state, [])
    state.valid()
    delta = datetime.now() - start
    do.log(RUN, f'final result after {state.getSteps()} steps using {delta} msec')
    showState(state, False)
    return state

def showState(state, showDetails):
    if do.isEnabled(RUN):
        do.log(RUN, state.toStringWithDetails(showDetails))

def runChallenge(challengeFileNameInFolderChallenges):
    print(f'trying to solve SUDOKU {challengeFileNameInFolderChallenges}')
    try:
        toSolve = readAllLines(f'_challenges/{challengeFileNameInFolderChallenges}', '')
        run(toSolve)
    except RuntimeError:
        print(f'The challenge file _challenges/{challengeFileNameInFolderChallenges} could not be read')

def readAllLines(name, sep):
    with open(name) as f:
        return sep.join(line.strip() for line in f)

if __name__ == "__main__":
    challengeFileNameInFolderChallenges = sys.argv[1]
    runChallenge(challengeFileNameInFolderChallenges)
