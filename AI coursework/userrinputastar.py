import re
from collections import Counter
from manhattandistances import a_star, print_board, Node


def parse_input(inputs)->(Node, Node, bool):
    """Method to parse the input of the 8-Puzzle UI
    
    Args
    inputs - List of each lineof user input
    
    Returns
    (Start_node, end_node, was the input valid)"""
    start_state_list = []
    end_state_list = []
    start_node = Node(state=[[],[],[]])
    end_node = Node(state=[[],[],[]])
    for i in range(0, len(inputs)):
        input_item = inputs[i]
        input_item = input_item.strip(" ")
        if(len(input_item) != 3):
            print("Invalid input")
            return (start_node, end_node, False)
        match_object = re.search("([_1-9]){3}",input_item)
        if match_object != None and i < 3:
            for character in input_item:
                if character == "_":
                    start_state_list.append(9)
                else:
                    start_state_list.append(int(character))
        elif match_object != None:
            for character in input_item:
                if character == "_":
                    end_state_list.append(9)
                else:
                    end_state_list.append(int(character))
        else:
            print("Invalid Input")
            return (start_node, end_node, False)
    tempdict = Counter(start_state_list)
    for item in tempdict:
        if tempdict[item] != 1:
            print("Invalid Input")
            return (start_node, end_node, False)
    tempdict = Counter(end_state_list)
    for item in tempdict:
        if tempdict[item] != 1:
            print("Invalid Input")
            return (start_node, end_node, False)
    start_node.state =[[start_state_list[0],start_state_list[1],start_state_list[2]],[start_state_list[3],start_state_list[4],start_state_list[5]],[start_state_list[6],start_state_list[7],start_state_list[8]]]
    end_node.state = [[end_state_list[0],end_state_list[1],end_state_list[2]],[end_state_list[3],end_state_list[4],end_state_list[5]],[end_state_list[6],end_state_list[7],end_state_list[8]]]
    return (start_node, end_node, True)

if __name__ == "__main__":
    input_list = []
    print("Start State:")
    input_list.append(input("Row 1 \n"))
    input_list.append(input("Row 2 \n"))
    input_list.append(input("Row 3 \n"))
    print("Goal State:")
    input_list.append(input("Row 1 \n"))
    input_list.append(input("Row 2 \n"))
    input_list.append(input("Row 3 \n"))
    out_tuple = parse_input(input_list)
    if out_tuple[2]:
        path = a_star(out_tuple[0],out_tuple[1])
        for item in path:
            print_board(item)
