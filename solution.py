assignments = []

rows = 'ABCDEFGHI' #rows of sudoku board
cols = '123456789' #columns of sudoku board

def cross(A, B):  #function to create box names on the board using cross product
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]

boxes = cross(rows, cols)  #box names of all 81 boxes on board

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#Diagonal units to solve DIAGONAL SUDOKU
#diag_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']]
diag_units = [[x+y for x, y in zip(rows, cols)], [x+y for x, y in zip(rows, cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units   #including diagonal units to original unit list

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)  #Generating dictionary of units for each box in sudoku board
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)   #Generation dictionary of peers for each box in sudoku board

def assign_value(values, box, value):  
    """
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    foo = []
    for item in grid:
        if item == '.':
            foo.append("123456789")
        else:
            foo.append(item)
    assert len(foo) == 81           #checking if grid provided has 81 boxes as it should
    return dict(zip(boxes,foo))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    #calulating maximum width of each box for display
    width = 1+max(len(values[s]) for s in boxes)
    #separating horizontal line between each 3x3 square      
    line = '+'.join(['-'*(width*3)]*3)                
    for r in rows:
        #printing values of sudoku according to box name
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')  
                      for c in cols))                                       
        if r in 'CF': print(line)                     
    print

def eliminate(values):      
    """Removes values from peers of solved boxes with only one possible value
    Args:
        values(dict): The sudoku in dictionary form
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    #list of boxes with two possible values
    tboxes = [box for box in values.keys() if len(values[box]) == 2]   

    for box in tboxes:
        val2check = values[box]
        #for each box, check the every unit of that box for its naked twin
        for unit in units[box]:     
            unit2up = False
            val2up = ''
            for unit_box in unit:
                #If naked twin found, store the string value to remove from all other boxes in that unit
                if (val2check == values[unit_box]) and (box!=unit_box):   
                    val2up = val2check                                    
                    unit2up = True                                        

            #Using constraint propagation remove the two values from all boxes in unit except the naked twins        
            if unit2up:   
                for unit_box in unit:
                    if (values[unit_box] != val2up) and (len(values[unit_box]) > 1):
                        values[unit_box] = ''.join(sorted(list(set(values[unit_box])-set(val2up))))

    return values

def only_choice(values):
    #Loop through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    valid = True
    while valid:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        valid = solved_values_before < solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    #Using depth-first search and propagation, try all possible values
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
