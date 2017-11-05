import os
import argparse
import sys
from heuristic import position

def parse_arg(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=open_file, help="the file must be a .txt")
    args = parser.parse_args()
    return args.file

def open_file(string):
    if not os.path.exists(string) or string[-4:] != '.txt':
        raise argparse.ArgumentTypeError("{0} is not a valid format or does not exist. Use --help for more informaion".format(string))
    return open(string, 'r')

def countInvertion(grid):
	length = len(grid)**2
	array = []

	for y, tab in enumerate(grid):
		for x, val in enumerate(tab):
			array.append(val)

	tot = 0
	for i, val1 in enumerate(array):
		for j in range(i + 1, length):
			val2 = array[j]
			if (val1 > val2 and val1 != 0 and val2 != 0):
				tot += 1
	return tot


def isSolvable(start, goal, dimension):
	startInversion = countInvertion(start)
	goalInversion = countInvertion(goal)
	if dimension % 2 == 0:
		starty, startx = position(start, 0)
		goaly, goalx = position(goal, 0)
		startInversion += starty
		goalInversion += goaly
	return (startInversion % 2 == goalInversion % 2)


if __name__ == "__main__":
	tab = [[7,6,1],[5,4,2],[0,8,3]]
	gridIsSolvable(tab)
