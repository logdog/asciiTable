#python 3
import argparse
import sys

# given a list of columns, see how many spaces it will take up
def getTotalSpaces(lst):
	pipes = len(lst) + 1
	scores = len(lst) * 2
	letters = 0
	for word in lst:
		for letter in word:
			letters += 1
	return pipes + scores + letters

def generateTopRow(lst):
	print('-' * getTotalSpaces(lst))

def generateHeader(lst):
	for word in lst:
		print('| ' + word + ' ', end='')
	print('|')

def generateRows(lst):
	for word in lst:
		print('| ' + (' ' * len(word)) + ' ', end='')
	print('|')

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--rows', type=int, default=4, help='Rows in table')
	parser.add_argument('-c', '--height', type=int, default=2, help='Height of cells in table')
	parser.add_argument('headers', nargs='+', help='Names of headers for each column')
	args = parser.parse_args()

	generateTopRow(args.headers)
	generateHeader(args.headers)
	generateTopRow(args.headers)

	for r in range(args.rows):
		for h in range(args.height):
			generateRows(args.headers)
		generateTopRow(args.headers)