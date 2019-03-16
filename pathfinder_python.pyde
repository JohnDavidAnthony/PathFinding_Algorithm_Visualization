add_library('controlP5')
import threading
import pathFunctions

# Listener for the textboxes to get user input
class TextListener(ControlListener):

    def controlEvent(self, e):
        global num_cols, num_rows
        if e.getName() == "width":
            num_cols = int(e.getStringValue())

        elif e.getName() == "height":
            num_rows = int(e.getStringValue())
            
        setupGrid()
        
# Listener for the buttons
class ButtonListener(ControlListener):

    def controlEvent(self, e):
        global mode
        if e.getName() == "start":
            mode = 0
        elif e.getName() == "goal":
            mode = 1
        elif e.getName() == "walls":
            mode = 2
        elif e.getName() == "empty":
            mode = 3
        elif e.getName() == "save":
            grid_to_text()
        elif e.getName() == "clear":
            clear()

global gridColour, saveGrid, num_cols, num_rows, boxWidth, boxHeight, mode, output, animation_time


def setup():
    global gridColour, saveGrid, num_cols, num_rows, boxWidth, boxHeight, mode
    
    size(1000, 1050)
    font = createFont("sansserif", 20)
    global cp5
    cp5 = ControlP5(this)
    
    # Call back functions
    def listenToClear(e):
        if e.getAction() == ControlP5.ACTION_RELEASED:
            clear()        
    
    cp5.addTextfield("width").setPosition(0, 0).setSize(
        200, 40).setFont(font).setFocus(True).setColor(color(255))
    
    cp5.addTextfield("height").setPosition(210, 0).setSize(
        200, 40).setFont(createFont("arial", 20))
    
    cp5.addBang("clear").setPosition(420, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("clear").addListener(ButtonListener())

    cp5.addBang("walls").setPosition(510, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("walls").addListener(ButtonListener())
    
    cp5.addBang("start").setPosition(600, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("start").addListener(ButtonListener())
    
    cp5.addBang("goal").setPosition(690, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("goal").addListener(ButtonListener())
    
    cp5.addBang("empty").setPosition(780, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("empty").addListener(ButtonListener())
    
    cp5.addBang("save").setPosition(870, 0).setSize(
        80, 40).getCaptionLabel().align(ControlP5.CENTER, ControlP5.CENTER)
    cp5.getController("save").addListener(ButtonListener())
    
    
    textFont(font)
    
    cp5.getController("width").addListener(TextListener())
    cp5.getController("height").addListener(TextListener())

    
    # Setup our Grid
    num_cols = 10
    num_rows = 10

    mode = 0
    setupGrid()

def draw():
    global gridColour, saveGrid, num_cols, num_rows, boxWidth, boxHeight
    background(50)

    for i in range(num_cols):
        for j in range(num_rows):
            if gridColour[i][j] == color(0):
                stroke(255); 
            else:
                stroke(0); 
            fill(gridColour[i][j]);
            rect(i*boxWidth, j*boxHeight + 70, boxWidth, boxHeight)

# Initalizes our grid to have a ring of walls and blank space
def setupGrid():
    global gridColour, saveGrid, num_cols, num_rows, boxWidth, boxHeight, output, animation_time
    
    # Create our writer
    output = createWriter("/Users/jd/Documents/GitHub/CISC352_Assignment2/Pathfinding/pathfinding_a.txt")
    
    # Offset for grid because of gui
    gridColour = [[0 for x in range(num_rows)] for x in range(num_cols)] 
    saveGrid = [[0 for x in range(num_rows)] for x in range(num_cols)] 
    
    boxWidth = width / num_cols
    boxHeight = (height-70) / num_rows

    # How long we want the animations to last
    animation_time = 15000 / (num_cols * num_rows)
          
    for i in range(num_cols):
        for j in range(num_rows):
            if i == 0 or j == 0 or i == num_cols-1 or j == num_rows-1:
                gridColour[i][j] = color(0)
                saveGrid[i][j] = 'X'
            else:
                gridColour[i][j] = color(255)
                saveGrid[i][j] = '_'

def draw_grid():
    global gridColour, saveGrid, num_cols, num_rows, boxWidth, boxHeight, mode
    for i in range(num_cols):
        for j in range(num_rows):
            x = i*boxWidth
            y = j*boxHeight
            if (mouseX > x and mouseX < (x + boxWidth) and mouseY-70 > y and mouseY-70< (y + boxHeight)):
                
                if (mode == 0):
                    gridColour[i][j] = color(255,0,0)
                    saveGrid[i][j] = 'S'
                elif (mode == 1):
                    gridColour[i][j] = color(0,255,0)
                    saveGrid[i][j] = 'G'
                elif (mode == 2):
                    gridColour[i][j] = color(0);
                    saveGrid[i][j] = 'X'
                else:
                    gridColour[i][j] = color(255);
                    saveGrid[i][j] = '_'
                    
def grid_to_text():
    global num_cols, num_rows, saveGrid, output
    for i in range(num_rows):
        line = ""
        for j in range(num_cols):
            line += saveGrid[i][j];
        output.println(line);
        print(line)
    output.flush() #  Writes the remaining data to the file
    output.close() #  Finishes the file

def keyPressed(): 
    global saveGrid
    
    # Greedy Cardinal Search
    if (key == 'g'):
        draw_grid()
        g = threading.Thread(target=greedy, args = (saveGrid,False, 2))
        g.daemon = True
        g.start()
    
    # A * Cardinal Search
    elif (key == 'a'):
        draw_grid()
        a = threading.Thread(target=a_star, args = (saveGrid,False, 2))
        a.daemon = True
        a.start()
        
    # Greedy Diagonal Search
    elif (key == 'h'):
        draw_grid()
        h = threading.Thread(target=greedy, args = (saveGrid, True, 1))
        h.daemon = True
        h.start()
        
    # A * Diagonal Search
    elif (key == 's'):
        draw_grid()
        s = threading.Thread(target=a_star, args = (saveGrid, True, 1))
        s.daemon = True
        s.start()
        
        
  

def mousePressed():
    draw_grid()
    
def mouseDragged():
    draw_grid()

def walls():
    global mode
    mode = 2

def clear():
    setupGrid()
    
# Sleeps the thread for delay ms, lazy approach
def sleep(delay):
    time = millis() 
    while(millis() - time <= delay):
        pass   

import queue as pq  # Priority queue library
# Start and goal are 2 value tuples and grid is a m*n grid
def greedy(grid, diagonal=False,  heuristic=1, start=None, goal=None):
    global gridColour
    
    # if no start or goal point entered, find them
    if not start:
        start = pathFunctions.get_point(grid, 'S')
    if not goal:
        goal = pathFunctions.get_point(grid, 'G')

    # Initialize our list with -1 in the dimensions of the grid
    came_from =[[-1] * len(grid[0]) for _ in range(len(grid))]

    # create our priority queue
    frontier = pq.PriorityQueue()
    frontier.put((1, start))

    # Set the value of start in the lists
    came_from[start[1]][start[0]] = None

    # While there are still possible paths
    while frontier.qsize():
        current = frontier.get()[1]
        
        #Set colour of current cell
        gridColour[current[1]][current[0]] = color(255, 233, 0)
        sleep(animation_time)
        
        if current == goal:
            # if we are currently at goal then stop
            path = pathFunctions.get_path(came_from, goal)
            animate_path(path)
            return


        # Get all of the current cell's neighbours
        neighbours = pathFunctions.get_neighbours(current, grid, diagonal)
        safe_neighbours = pathFunctions.check_neighbours(neighbours, grid)
        for neighbour in safe_neighbours:
            
            if came_from[neighbour[1]][neighbour[0]] == -1:
                # Set colour of neighbour
                gridColour[neighbour[1]][neighbour[0]] = color(204, 191, 201)
                sleep(animation_time)
            
                # Use the selected heuristic
                if heuristic == 1:
                    priority = pathFunctions.euclidean((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                elif heuristic == 2:
                    priority = pathFunctions.manhattan((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                elif heuristic == 3:
                    priority = pathFunctions.chebyshev((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                else:
                    # Greedy
                    priority = 1

                frontier.put((priority, neighbour))
                came_from[neighbour[1]][neighbour[0]] = current
            # Set colour of neighbour back as we are about to switch
            #gridColour[neighbour[1]][neighbour[0]] = color(50)
            
        # Set colour of current cell back as we are about to switch
        gridColour[current[1]][current[0]] = color(124, 114, 0)

    return None

# Start and goal are 2 value tuples and grid is a m*n grid
def a_star(grid, diagonal=False,  heuristic=1, start=None, goal=None):
    global gridColour, animation_time
    # if no start or goal point entered, find them
    if not start:
        start = pathFunctions.get_point(grid, 'S')
    if not goal:
        goal = pathFunctions.get_point(grid, 'G')

    # Initialize our lists with -1 in the dimensions of the grid
    came_from =[[-1] * len(grid[0]) for _ in range(len(grid))]
    cost_so_far = [[-1] * len(grid[0]) for _ in range(len(grid))]

    # create our priority queue
    frontier = pq.PriorityQueue()
    frontier.put((1, start))

    # Set the value of start in the lists
    came_from[start[1]][start[0]] = None
    cost_so_far[start[1]][start[0]] = 0

    # While there are still possible paths
    while frontier.qsize():
        current = frontier.get()[1]
        
        #Set colour of current cell
        gridColour[current[1]][current[0]] = color(255, 233, 0)
        sleep(animation_time)

        if current == goal:
            # if we are currently at goal then stop
            path = pathFunctions.get_path(came_from, goal)
            animate_path(path)
            return

        # Get all of the current cell's neighbours
        neighbours = pathFunctions.get_neighbours(current, grid, diagonal)
        safe_neighbours = pathFunctions.check_neighbours(neighbours, grid)
        for neighbour in safe_neighbours:
            #TODO Determine what the cost is to go from current to neighbour
            new_cost = cost_so_far[current[1]][current[0]] + 1

            # Check to see if we have already seen neighbour or the new cost of the neighbour is < cost so far
            if new_cost < cost_so_far[neighbour[1]][neighbour[0]] or cost_so_far[neighbour[1]][neighbour[0]] == -1:
                # Set colour of neighbour
                gridColour[neighbour[1]][neighbour[0]] = color(204, 191, 201)
                sleep(animation_time)
                
                cost_so_far[neighbour[1]][neighbour[0]] = new_cost

                # Use the selected heuristic
                if heuristic == 1:
                    heuristic_value = pathFunctions.euclidean((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                elif heuristic == 2:
                    heuristic_value = pathFunctions.manhattan((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                elif heuristic == 3:
                    heuristic_value = pathFunctions.chebyshev((goal[1], goal[0]), (neighbour[1], neighbour[0]))
                else:
                    heuristic_value = 0

                priority = new_cost + heuristic_value
                frontier.put((priority, neighbour))
                came_from[neighbour[1]][neighbour[0]] = current
                
        # Set colour of current cell back as we are about to switch
        gridColour[current[1]][current[0]] = color(124, 114, 0)

    return None

def animate_path(path):
    global gridColour, animation_time
    for i in range(len(path)):
        gridColour[path[i][1]][path[i][0]] = color(0, 0, 201)
        sleep(50)
        gridColour[path[i][1]][path[i][0]] = color(0, 0, 150)
        
    sleep(1000)
    
    for i in range(len(path)-1, -1, -1):
        gridColour[path[i][1]][path[i][0]] = color(0, 0, 201)
        sleep(50)
        gridColour[path[i][1]][path[i][0]] = color(0, 0, 150)
