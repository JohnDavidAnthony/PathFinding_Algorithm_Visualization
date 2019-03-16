import searchAlgs
import copy

def readInFile(fileName):
    # Code to read in the pathfinding txt file
    problemSet = []
    singleGrid = []
    with open(fileName, 'r') as inputFile:
        for line in inputFile:
            try:
                if line == "\n":  # Have read in all of the grid
                    problemSet.append(singleGrid)
                    singleGrid = []
                else:
                    singleGrid.append(list(line.rstrip()))

            except:
                print("Error with input file")
                exit(1)
        problemSet.append(singleGrid) # Append the last grid
        inputFile.close()

    return problemSet

def grid_to_file(filename, grid_string):
    with open(filename,'w') as outputFile:
        outputFile.write(grid_string)
        outputFile.close()


# Takes a grid and list of x,y co-ords and returns an updated grid replaced with char
def update_grid(grid, path, char='P'):
    for step in path:
        grid[step[1]][step[0]] = char

    return grid


# Takes a grid and returns a string in the format of the project
def grid_to_string(grid):
    grid_str = ''

    for row in grid:
        for col in row:
            grid_str += col + ' '
        grid_str += '\n'

    return grid_str


if __name__ == "__main__":
    cardinalGrids = readInFile("pathfinding_a.txt")
    diagonalGrids = readInFile("pathfinding_b.txt")

    # Cardinal Grids
    cardinalString = ""
    for grid in cardinalGrids:
        # Greedy
        cardinalString += "Greedy\n"
        gridCopy = copy.deepcopy(grid)
        star_path = searchAlgs.a_star(gridCopy, False, 0)
        new_grid = update_grid(gridCopy, star_path)
        grid_str = grid_to_string(new_grid)
        cardinalString += grid_str + '\n'

        # A*
        cardinalString += "A*\n"
        gridCopy = copy.deepcopy(grid)
        star_path = searchAlgs.a_star(gridCopy, False, 2)
        new_grid = update_grid(gridCopy, star_path)
        grid_str = grid_to_string(new_grid)
        cardinalString += grid_str + '\n'

    diagonalString = ""
    for grid in diagonalGrids:
        # Greedy
        diagonalString += "Greedy\n"
        gridCopy = copy.deepcopy(grid)
        star_path = searchAlgs.a_star(gridCopy, True, 1)
        new_grid = update_grid(gridCopy, star_path)
        grid_str = grid_to_string(new_grid)
        diagonalString += grid_str + '\n'

        # A*
        diagonalString += "A*\n"
        gridCopy = copy.deepcopy(grid)
        star_path = searchAlgs.a_star(gridCopy, True, 0)
        new_grid = update_grid(gridCopy, star_path)
        grid_str = grid_to_string(new_grid)
        diagonalString += grid_str + '\n'

    grid_to_file("pathfinding_a_out.txt", cardinalString)
    grid_to_file("pathfinding_b_out.txt", diagonalString)
