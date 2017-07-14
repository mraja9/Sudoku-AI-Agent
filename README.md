## AI agent to solve Sudoku
The AI agent in this project solves Diagonal Sudokus using constraint propagation and search techniques. Additionally, taught the agent to use the Naked Twins advanced Sudoku strategy.
    
[Sudoku strategy](http://sudokudragon.com/sudokustrategy.htm)
* Only choice rule
* Single possibility rule
* Naked Twin exclusion rule

**Constraint propagation**  
Functions **eliminate** and **naked_twins** in ```solution.py``` use constraint propagation.

**Search**    
Used recursion techniques to create depth-first-search trees for solving hard sudokus.

## Install

This project requires **Python 3**. Clone the repo and run solution.py or solution_test.py (unit tests).


## Data

The data consists of a text file of unsolved diagonal sudokus.

## License

MIT License.