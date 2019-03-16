import math
import queue as pq  # Priority queue library

# point is a 2 value tuple (x,y), grid is a m*n grid, diagonal bool determines if we return diagonal neighbours
# returns a list of tuple neighbours
def get_neighbours(point, grid, diagonal=False):
    pointx = point[0]
    pointy = point[1]
    # Check the corners so we don't go our of bounds

    if pointx == 0:
        # we are at left side of grid
        if pointy == 0:
            # we are at top left corner of grid
            if diagonal:
                return [(pointx + 1, pointy), (pointx + 1, pointy + 1), (pointx, pointy + 1)]
            return [(pointx + 1, pointy), (pointx, pointy + 1)]

        elif pointy == len(grid) - 1:
            # we are at bottom left corner of grid
            if diagonal:
                return [(pointx + 1, pointy), (pointx + 1, pointy - 1), (pointx, pointy - 1)]
            return [(pointx + 1, pointy), (pointx, pointy - 1)]

        else:
            # we are at middle left of grid
            if diagonal:
                return [(pointx, pointy - 1), (pointx + 1, pointy - 1), (pointx + 1, pointy), (pointx + 1, pointy + 1),
                        (pointx, pointy + 1)]
            return [(pointx, pointy - 1), (pointx + 1, pointy), (pointx, pointy + 1)]

    elif pointx == len(grid[0]) - 1:
        # we are at right side of grid
        if pointy == 0:
            # we are at top right corner of grid
            if diagonal:
                return [(pointx - 1, pointy), (pointx - 1, pointy + 1), (pointx, pointy + 1)]
            return [(pointx - 1, pointy), (pointx, pointy + 1)]

        elif pointy == len(grid) - 1:
            # we are at bottom right corner of grid
            if diagonal:
                return [(pointx - 1, pointy), (pointx - 1, pointy - 1), (pointx, pointy - 1)]
            return [(pointx - 1, pointy), (pointx, pointy - 1)]

        else:
            # we are at middle right of grid
            if diagonal:
                return [(pointx, pointy - 1), (pointx - 1, pointy - 1), (pointx - 1, pointy), (pointx - 1, pointy + 1),
                        (pointx, pointy + 1)]
            return [(pointx, pointy - 1), (pointx - 1, pointy), (pointx, pointy + 1)]

    elif pointy == 0:
        # we are on top middle of grid
        if diagonal:
            return [(pointx + 1, pointy), (pointx + 1, pointy + 1), (pointx, pointy + 1), (pointx - 1, pointy + 1),
                    (pointx - 1, pointy)]
        return [(pointx + 1, pointy), (pointx, pointy + 1), (pointx - 1, pointy)]

    elif pointy == len(grid) - 1:
        if diagonal:
            return [(pointx + 1, pointy), (pointx + 1, pointy - 1), (pointx, pointy - 1), (pointx - 1, pointy - 1),
                    (pointx - 1, pointy)]
        return [(pointx + 1, pointy), (pointx, pointy - 1), (pointx - 1, pointy)]

    # Not on the edges, we wont go our of bounds
    if diagonal:
        return [(pointx - 1, pointy), (pointx - 1, pointy - 1), (pointx, pointy - 1), (pointx + 1, pointy - 1),
                (pointx + 1, pointy), (pointx + 1, pointy + 1), (pointx, pointy + 1), (pointx - 1, pointy + 1)]
    return [(pointx - 1, pointy), (pointx, pointy - 1), (pointx + 1, pointy), (pointx, pointy + 1)]


# takes a list of x,y tuples and the grid and only returns the tuples that are not obstacles ("X")
def check_neighbours(neighbours, grid):
    new_neighbours = []
    for neighbour in neighbours:
        if grid[neighbour[1]][neighbour[0]] != "X":
            new_neighbours.append(neighbour)

    return new_neighbours


# Returns the (x,y) tuple location of the first location of char
def get_point(grid, char):
    i,j = -1,-1
    for row in grid:
        for elem in row:
            if(elem == char):
                return(row.index(elem), grid.index(row))
    return(None)


# returns the path from the came_from array
def get_path(came_from, goal):
    current = goal
    path = []
    # Work back wards from the goal to build the path
    while current != None:
        path.append(current)
        current = came_from[current[1]][current[0]]

    path.reverse()
    return path

# Heuristic Functions

# Option 1
def euclidean(a, b):
    return math.sqrt(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2))

# Option 2
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Option 3
def chebyshev(a, b):
    return max(abs(b[0] - a[0]), abs(b[1] - a[1]))

# Option 4
def greedy(a, b):
    return 0
