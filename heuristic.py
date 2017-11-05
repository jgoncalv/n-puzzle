import math

def position(lst2d, value):
	return next((y, x) for y, lst in enumerate(lst2d) for x, val in enumerate(lst) if val == value)


def h_manhattan(curGrid, askGrid):
	l = len(curGrid[0])**2 
	tot = 0
	for i in range(1, l):
		curY, curX = position(curGrid, i)
		askY, askX = position(askGrid, i)
		dx = abs(curX - askX)
		dy = abs(curY - askY)
		tot += dx + dy
	return tot

def h_misplaced(curGrid, askGrid):
	l = len(curGrid[0])**2
	tot = 0
	for i in range(1, l):
		if (position(curGrid, i) != position(askGrid, i)):
			tot += 1
	return tot

def h_linear(curGrid, askGrid):
	h = h_manhattan(curGrid, askGrid)
	line = 0
	l = len(curGrid[0])**2
	for i in range(1, l):
		y, x = position(curGrid, i)
		yf, xf = position(askGrid, i)
		if (bool(y == yf) != bool(x == xf)):
			line += 1
	return h + 2 * line
