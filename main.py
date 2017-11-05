#!/usr/bin/python3

import sys
from models import Node
from parse import parse_arg, isSolvable
from astar import a_star

def get_goal(dimension):
    '''Generate final solved grid'''
    total_size = dimension * dimension
    goal = [-1 for i in range(total_size)]
    current = 1
    x = 0
    i_x = 1
    y = 0
    i_y = 0
    while 42:
        goal[x + y * dimension] = current
        if current == 0:
            break
        current += 1
        if x + i_x == dimension or x + i_x < 0 or (i_x != 0 and goal[x + i_x + y * dimension] != -1):
            i_y = i_x
            i_x = 0
        elif y + i_y == dimension or y + i_y < 0 or (i_y != 0 and goal[x + (y + i_y) * dimension] != -1):
            i_x = -i_y
            i_y = 0
        x += i_x
        y += i_y
        if current == dimension * dimension:
            current = 0
    goal = [goal[x:x+dimension] for x in range(0,len(goal),dimension)]
    return goal

def readfile(fd):
    table = []
    for l in fd.readlines():
        l = ' '.join(l.split())
        table.append(l.split('#', 1)[0])
    table = [x for x in table if x]
    dimension = int(table.pop(0))
    for i, s in enumerate(table):
        table[i] = table[i].split()
        if len(table[i]) is not dimension:
            print("Wrong file format")
            sys.exit()
    for i, s in enumerate(table):   
        table[i] = [int(i) for i in table[i]]
    for number in range(dimension ** 2):
        flag = 0
        for line in table:
            if number in line:
                flag = 1
        if flag % 2 == 0:
            print("Wrong numbers in file")
            sys.exit()        
    return table, get_goal(dimension), dimension

def main(argv):
    fd = parse_arg(argv)
    start, goal, dimension = readfile(fd)
    if not isSolvable(start, goal, dimension):
        print("This puzzle cannot be solved. Try generating another one.")
        sys.exit()
    start = Node(start)
    items = {'1': 'Manhattan Distance', '2': 'Misplaced Tiles', '3': 'Linear Conflict', '4': 'Greedy BFS', '5': 'Dijkstra'}
    choice = input("Welcome to our n-puzzle program. Please choose between the 3 following heuristics to solve the problem :\n 1: 'Manhattan Distance'\n 2: 'Misplaced Tiles'\n 3: 'Linear Conflict'\n 4: 'Greedy BFS [bonus]'\n 5: 'Dijkstra [bonus]'\n Select your heuristic (1, 2, 3, 4 or 5): ")
    if choice in items:
        heuristic = items[choice]
    else:
        print("Not a correct value")
        sys.exit()
    res, closedlist, openlist, num_moves = a_star(start, goal, heuristic)
    time_complex = len(closedlist)
    size_complex = len(openlist) + time_complex
    for i in res:
        print("Move", i.g)
        for l in i.grid:
            line = []
            for n in l:
                line.append(n)
            print(*line, sep=' ')
        print("\n")
    print("Time complexity: ", time_complex)
    print("Size complixity: ", size_complex)
    print("Total number of moves", num_moves)


if __name__ == "__main__":
    main(sys.argv[1:])