import operator
import copy
from heuristic import position, h_manhattan, h_misplaced, h_linear
from models import Node

def lower_seen(lst, co):
    #Return True only if node "co" is already in list lst with a lower cost.
    for l in lst:
        if co.grid == l.grid:
            if co.f < l.f:
                return False
            else:
                return True
    return False

def build_path(start, testing):
    #Recreate the path to have the following list as the return of the a_star function : [start, node1, node2, ..., nodeX, goal]
    path = [testing]
    p = testing.parent
    while p.grid != start.grid:
        path.append(p)
        p = p.parent
    path.append(start)
    return list(reversed(path))

def get_next_moves(current):
    moves = []
    zeroY, zeroX = position(current.grid, 0)
    gridsize = len(current.grid[0])
    if zeroY + 1 < gridsize:
        a = copy.deepcopy(current.grid)
        a[zeroY + 1][zeroX], a[zeroY][zeroX] = a[zeroY][zeroX], a[zeroY + 1][zeroX]
        if a != current.grid:
            moves.append(Node(a))
    if zeroY - 1 > -1:
        b = copy.deepcopy(current.grid)
        b[zeroY - 1][zeroX], b[zeroY][zeroX] = b[zeroY][zeroX], b[zeroY - 1][zeroX]
        if b != current.grid:
            moves.append(Node(b))
    if zeroX + 1 < gridsize:
        c = copy.deepcopy(current.grid)
        c[zeroY][zeroX + 1], c[zeroY][zeroX] = c[zeroY][zeroX], c[zeroY][zeroX + 1]
        if c != current.grid:
            moves.append(Node(c))
    if zeroX - 1 > -1:
        d = copy.deepcopy(current.grid)
        d[zeroY][zeroX - 1], d[zeroY][zeroX] = d[zeroY][zeroX], d[zeroY][zeroX - 1]
        if d != current.grid:
            moves.append(Node(d))
    for node in moves:
        node.parent = current
    return (moves)

def a_star(start, goal, heuristic):
    if heuristic == "Manhattan Distance":
        start.update(0, h_manhattan(start.grid, goal), False)
    elif heuristic == "Misplaced Tiles":
        start.update(0, h_misplaced(start.grid, goal), False)
    elif heuristic == "Linear Conflict":
        start.update(0, h_linear(start.grid, goal), False)
    elif heuristic == "Dijkstra":   
        start.update(0, 0, False)   
    else:
        start.update(0, h_manhattan(start.grid, goal), True) 
    #If both grids are the same, return the distance between them
    if start.grid == goal:
            return (0)
    #Create open and closed lists, add the starting node to the open list
    openlist = []
    closedlist = []
    openlist.append(start)
    #Loop continue until the open list becomes empty or we find the goal
    while openlist:
        #Evaluate first node in open list
        current = openlist[0]
        #If that node is our goal, return the full path as a list and the total distance from start to goal
        if current.grid == goal:
            return build_path(start, current), closedlist, openlist, current.g
        #Create next moves as nodes
        children = get_next_moves(current)
        #Evaluate our node's children
        for child in children:
            #Evaluate cost of getting from start to testing's child node
            g = current.g + 1
            if heuristic == "Misplaced Tiles":
                h = h_misplaced(child.grid, goal)
            elif heuristic == "Linear Conflict":
                h = h_linear(child.grid, goal)  
            elif heuristic == "Dijkstra":   
                h = 0      
            else:
                h = h_manhattan(child.grid, goal)
            if heuristic == "Greedy BFS":
                child.update(g, h, True)
            else:
                child.update(g, h, False)
            #If child node is already on openlist or closedlist with a lower cost, we pass
            if lower_seen(openlist, child) or lower_seen(closedlist, child):
                pass
            #Else, we ponderate the cost of getting to that child node with it's heuristic distance to the goal.
            #Then we add the child node to the openlist or replace it if already present with a higher cost.
            else:
                if child in openlist:
                    openlist = [child if x.grid == child.grid else x for x in openlist]
                else:
                    openlist.append(child)
        #Once all its connections are evaluated, we remove the node from openlist and add it or replace it in closedlist
        del(openlist[0])
        if current in closedlist:
            closedlist = [current if x.grid == current.grid else x for x in closedlist]
        else:
            closedlist.append(current)
        #Sort open list so that the node with the lower heuristic cost is evaluated first
        openlist = sorted(openlist, key=operator.attrgetter('f'))
    return ("no existing path")