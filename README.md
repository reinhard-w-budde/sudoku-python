only for testing pull requests#

# SUDOKU

## Overview

There are hundreds of Sudoku solvers on Github alone. Why another one? The sources are written to show good software engineering practices.
Or at least I try to do this :-). Or at least I try to stimulate discussions about that topic :-). So participate!

It is open-source and can be changed and used for private purposes without any restriction. See the LICENCE file.

This git repository contains a Python >=3.6 solution. Other languages, I use, will be addressed, too:

* Java (https://github.com/reinhard-w-budde/sudoku-java.git )
* Python (this Git repo,  https://github.com/reinhard-w-budde/sudoku-java.git )
* Go,
* Typescript (implies a Javascript solution).

## Model of the solver

* a soduku (class 'State' in module 'sudoku/state') contains 81 cells (class 'Cell' in module 'sudoku/cell') numbered from 1 to 81.
* each cell contains the list of possible values (1...9) for this cell. If the list has exactly one item, the cell's value is discovered.
* each cell has 3 neighborhoods (module 'sudoku/structure'), called horizontal, vertical and group neighborhood.
* each of the 27 neighborhoods (each contains 9 cells) doesn't allow that two of its cell have the same value.

* a soduku is read (for exapmple in module 'tests/sudoku_test') from a file (stored in directory '_examples' with the name 'sudoku-<two-digit-number>')
* an initial state is constructed (module 'sudoku/runsoduku').
* this state is transformed to a state, that is closer to the final solution (module 'sudoku/runsoduku') by applying rules (module 'sudoku/rulemachine').

* O: rule 'ruleOneValLeft' is the simplest one: it looks, whether a cell has only one possible value. If yes, a solution is found and the rule
  calls itself recursively.
  
* E: rule 'ruleExcludedVal' is of medium complexity: it takes a possible value of a cell and looks into the cell's 3 neighborhoods to check whether in on
  of the neighborhoods this value is impossible for all (other) cells. If yes, then a solution is found. The first rule 'ruleOneValLeft' is called
  again, then the rule calls itself recursively.
  
* remark: if a solution is found for a cell, this knowledge is propagated by removing the value found from the set of possible values of all cells of
  its 3 neighborhoods.
  
* B: rule 'backtrack' is the most complex rule: it takes a cell as a 'test cell', fixes one of its possible values as a temporary solution and tries to solve the sodok
  by calling 'ruleOneValLeft' and 'ruleExcludedVal'.
  * if no inconsistency is detected, the rule selects recursively another cell until the sudoku is solved.
  * if an inconsistency is detected ('FAIL'), the next possible value from the 'test cell' is taken. If all values are exhausted, the sudoku is unsolvable.
  * to improve performance, that cell is selected as the 'test cell', which has the least number (>=2) of possible values left.

* that's all.

## Requirements for Python

* Python on the path. Versions must be >= 3.6 as f-strings are used
* Git. It is great, that after installation (on windows) you get a bash shell for free.

* Eclipse Photon. Older versions will do as well. Eclipse integration of Git is good. Install the PyDev plugin.

Eclipse is not strictly needed. If you have experiences with other programming environments, that's fine. 
  
## Work with Pythonn

1. create a directory for your git repositories, e.g. "git"
```sh
    mkdir git; cd git
```

2. get the git repository. It contains the branch master.
```sh
    git clone https://github.com/reinhard-w-budde/sudoku-python.git
    cd sudoku-python
```

3. test. All sudokus from the '_examples' folder will be solved as tests and compared with the solutions in '_solutions'.
   Run from the project base directory
```sh
    python -m unittest tests/*.py || echo -e '\n===========\nTEST FAILED\n===========\n'
```

4. put sudokus into files which you want to solve, for examples into folder '_challenges'. Run from the project base directory
```sh
    python sudoku/runsudoku.py _challenges/YOUR_FILE_NAME
```

5. For suggestions, discussions, questions, proposals for a better programming style contact me at reinhard.budde at iais.fraunhofer.de
