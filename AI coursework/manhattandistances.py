from queue import PriorityQueue

class Node():
    """Class to represent a node in the board space"""
    def __init__(self, parent=None, state=None):
        self.parent_node = parent
        self.state = [list(state[0]),list(state[1]), list(state[2])]

        self.cost = 0
        self.heuristic = 0
        self.estimate = 0
        self.depth = 0

    def __eq__(self, other):
        """Built in method for equalities"""
        if self.state[0] == other.state[0] and self.state[1] == other.state[1] and self.state[2] == other.state[2]:
            return True
        else: 
            return False

    def __str__(self):
        """Built in method for string representation"""
        return str(self.state)

    def __repr__(self):
        """Built in method for printing representation"""
        return str(self.state)

    def __lt__(self, other):
        """Built in method for comparison representation"""
        return self.estimate < other.estimate

def print_board(board_state:list):
    """Function to pretty print a board state

    Args
    board_state - Board to print"""
    print(board_state[0])
    print(board_state[1])
    print(board_state[2])
    print("\n")

def manhattan_heuristic(current_state:list, goal_state:list)->int:
    """Heuristic function to find the distance to the goal state using manhattan blocks technique

    Args
    current_state - The current_state of the puzzle
    goal_state - The goal state of the puzzle

    Returns an integer value for the manhattan blocks number"""
    current = {}
    goal = {}
    manhattan_blocks = 0
    for row in range(0, 3):
        for tile in range(0,3):
            current_value = current_state[row][tile]
            desired_value = goal_state[row][tile]
            current[current_value] = (row, tile)
            goal[desired_value] = (row, tile)
    for item, coord in current.items():
        diffrow = abs(goal[item][0] - coord[0])
        difftile = abs(goal[item][1] - coord[1])
        manhattan_blocks += diffrow +difftile
    return manhattan_blocks

def move_left(current_node:list)->list:
    """Moves the blank space (represented by a 9) left
    
    Args
    node - list which reprsents the board state to move left

    Returns a list representing the board with the blank moved left"""
    node = [list(current_node[0]),list(current_node[1]),list(current_node[2])]
    coordinate = []
    target_coordinate = []
    target_value = 0
    temp_value = 0
    for row in range(0,3):
        for tile in range(0,3):
            temp_value = node[row][tile]
            if temp_value == 9:
                coordinate = [row,tile]
                break
    if coordinate[1] == 0:
        return None
    target_coordinate = [coordinate[0], coordinate[1] - 1]
    target_value = node[target_coordinate[0]][target_coordinate[1]]
    node[target_coordinate[0]][target_coordinate[1]] = 9
    node[coordinate[0]][coordinate[1]] = target_value
    return node

def move_right(current_node:list)->list:
    """Moves the blank space (represented by a 9) right
    
    Args
    node - list which reprsents the board state to move right

    Returns a list representing the board with the blank moved right"""
    node = [list(current_node[0]),list(current_node[1]),list(current_node[2])]
    coordinate = []
    target_coordinate = []
    target_value = 0
    temp_value = 0
    for row in range(0,3):
        for tile in range(0,3):
            temp_value = node[row][tile]
            if temp_value == 9:
                coordinate = [row,tile]
                break
    if coordinate[1] == 2:
        return None
    target_coordinate = [coordinate[0], coordinate[1] + 1]
    target_value = node[target_coordinate[0]][target_coordinate[1]]
    node[target_coordinate[0]][target_coordinate[1]] = 9
    node[coordinate[0]][coordinate[1]] = target_value
    return node

def move_up(current_node:list)->list:
    """Moves the blank space (represented by a 9) up
    
    Args
    node - list which reprsents the board state to move up

    Returns a list representing the board with the blank moved up"""
    node = [list(current_node[0]),list(current_node[1]),list(current_node[2])]
    coordinate = []
    target_coordinate = []
    target_value = 0
    temp_value = 0
    for row in range(0,3):
        for tile in range(0,3):
            temp_value = node[row][tile]
            if temp_value == 9:
                coordinate = [row,tile]
                break
    if coordinate[0] == 0:
        return None
    target_coordinate = [coordinate[0] - 1, coordinate[1]]
    target_value = node[target_coordinate[0]][target_coordinate[1]]
    node[target_coordinate[0]][target_coordinate[1]] = 9
    node[coordinate[0]][coordinate[1]] = target_value
    return node

def move_down(current_node:list)->list:
    """Moves the blank space (represented by a 9) dwon
    
    Args
    node - list which reprsents the board state to move down

    Returns a list representing the board with the blank moved down"""
    node = [list(current_node[0]),list(current_node[1]),list(current_node[2])]
    coordinate = []
    target_coordinate = []
    target_value = 0
    temp_value = 0
    for row in range(0,3):
        for tile in range(0,3):
            temp_value = node[row][tile]
            if temp_value == 9:
                coordinate = [row,tile]
                break
    if coordinate[0] == 2:
        return None
    target_coordinate = [coordinate[0] + 1, coordinate[1]]
    target_value = node[target_coordinate[0]][target_coordinate[1]]
    node[target_coordinate[0]][target_coordinate[1]] = 9
    node[coordinate[0]][coordinate[1]] = target_value
    return node

def a_star(start_node: Node, end_node: Node)->list:
    """Performs A* path finding between two nodes using manhattan distances as the heuristic function.

    Args
    start_node - Start state node
    end_node - Goal state node
    
    Returns
    List of nodes for the optimal path"""
    open_nodes= PriorityQueue()
    closed_nodes = []
    solved = False
    open_nodes.put((1,start_node))
    loops = 0
    while not open_nodes.empty():
        loops += 1
        current_node = open_nodes.get()[1]
        closed_nodes.append(current_node)
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.state)
                current = current.parent_node
            return path[::-1]

        child_nodes = []
        left_state = None
        right_state = None
        up_state = None
        down_state = None
        left_state = move_left(current_node.state)
        right_state = move_right(current_node.state)
        up_state = move_up(current_node.state)
        down_state = move_down(current_node.state)
        if left_state != None:
            left_node = Node(current_node, left_state)
            child_nodes.append(left_node)
        if right_state != None:
            right_node = Node(current_node, right_state)
            child_nodes.append(right_node)
        if up_state != None:
            up_node = Node(current_node, up_state)
            child_nodes.append(up_node)
        if down_state != None:
            down_node = Node(current_node, down_state)
            child_nodes.append(down_node)
        for child_node in child_nodes:
            already_open = False
            if child_node not in closed_nodes and current_node != child_node:
                child_node.cost = current_node.cost + 1
                child_node.heuristic = manhattan_heuristic(child_node.state, end_node.state)
                child_node.estimate = child_node.cost + child_node.heuristic
                child_node.depth = current_node.depth + 1
                if not already_open:            
                    open_nodes.put((child_node.estimate, child_node))
        if len(closed_nodes) > 362880:
            print("Error")

if __name__ == "__main__":
    start_state = [[7,2,4],[5,9,6],[8,3,1]]
    goal_state = [[9,1,2],[3,4,5],[6,7,8]]
    start_node = Node(None, start_state)
    goal_node = Node(None, goal_state)
    result = a_star(start_node,goal_node)
    for item in result:
        print_board(item)