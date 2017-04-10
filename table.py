# python 3.5
import sys
import math
from collections import OrderedDict

MAX_TRIES = 100000

class Cell:
    def __init__(self, text, padding=0):
        self.text = str(text)
        self.padding = padding
        self.lines = [" "*self.padding + self.text + " "*self.padding]
        self.total_chars = len(self.text) + 2*self.padding
        self.depth = len(self.lines)

    def get_depth(self):
        return self.depth

    def get_line(self, index):
        try:
            return self.lines[index]
        except:
            return ""

    def get_width(self):
        return len(self.lines[0])

    def remove_depth(self):
        self.depth -= 1
        max_chars_per_line = math.ceil(self.total_chars / self.depth)
        for index,_ in enumerate(self.lines):
            self.lines[index] =  " "*self.padding + self.text[index*max_chars_per_line: (index+1)*max_chars_per_line] + " "*self.padding
        self.lines = self.lines[:-1]
        return self.depth

    def add_depth(self):
        self.depth += 1
        self.lines.append(None)
        # does not include padding as a char in a line here
        max_chars_per_line = math.ceil(self.total_chars / self.depth)
        for index,_ in enumerate(self.lines):
            self.lines[index] =  " "*self.padding + self.text[index*max_chars_per_line: (index+1)*max_chars_per_line] + " "*self.padding
        return self.depth

class Column(Cell):
    def __init__(self, text, padding=0):
        super().__init__(text, padding=padding)
        self.daughter_cells = []
        self._index = 0

    def add_cell(self, text):
        self.daughter_cells.append(Cell(text))

    def add_depth(self):
        # super().add_depth()
        for c in self.daughter_cells: 
            c.add_depth()

    def add_my_depth(self):
        return super().add_depth()

    def get_depth(self):
        # returns the column's deepest depth value
        col_depth = super().get_depth()
        for c in self.daughter_cells:
            col_depth = max(col_depth, c.get_depth())
        return col_depth

    def get_width(self):
        # returns the colum's largest width value
        max_width = super().get_width()
        for c in self.daughter_cells:
            max_width = max(max_width, c.get_width())
        return max_width

    def get_my_width(self):
        return super().get_width()

    def get_total_daughters(self):
        return len(self.daughter_cells)

    def get_cell(self, index):
        try:
            return self.daughter_cells[index]
        except:
            return Cell("")

class Table():
    '''
    data = {
        key1: [data1, data2, data3],
        key2: [data4, data5, data6]
    }

    key1    key2

    data1   data4
    data2   data5
    data3   data6

    '''

    def __init__(self, data, max_total_width=162, padding=0, fast_mode=False):
        self.columns = []
        self.fast_mode = fast_mode
        # populate columns
        # then add them to the table
        for key, value in data.items():
            col = Column(key, padding=padding)
            for datax in value:
                col.add_cell(datax)
            self.columns.append(col)

        # adjust sizing
        tries = 0
        current_total_width = 1000000001 # a billione

        # fast mode
        # assume all data is similar, and use the 0th
        # row as a model to assume the rest of the tbale
        min_table_width = 2*(len(self.columns)) + 1
        if max_total_width < min_table_width:
            print("ERROR: minimum table width for this dataset is %d. Will generate this size instead." % (min_table_width))
            max_total_width = min_table_width

        if self.fast_mode:
            while current_total_width > max_total_width:
                tries += 1
                max_cell_value = 0 # starts at 0 grows to max width
                max_col_index = 0  # i
                max_cell_index = -1   # -1 or 0

                for i, col in enumerate(self.columns):
                    header_title_width = col.get_my_width()
                    row_0_cell_width = col.daughter_cells[0].get_width()

                    if header_title_width > max_cell_value:
                        max_cell_index = -1
                        max_col_index = i
                        max_cell_value = header_title_width

                    if row_0_cell_width > max_cell_value:
                        max_cell_index = 0
                        max_col_index = i
                        max_cell_value = row_0_cell_width

                if max_cell_index == -1:
                    # add depth to just the title
                    self.columns[max_col_index].add_my_depth()
                else:
                    # add depth to everything
                    self.columns[max_col_index].add_depth()

                current_total_width = self.get_current_width()
                if tries >= MAX_TRIES:
                    print("ERROR: Could not make table to desired width. Attempts tried: %d" % (tries))
                    break

        else:
            # comprehensive mode
            # find largest cell, shrink it
            while current_total_width > max_total_width:
                cells_to_update = [] # list of tuples: col index, cell index. -1 cell index == the column header itself
                tries += 1
                # find column with largest entry stored at max_index
                # that has 
                max_cell_width = 0

                for i, col in enumerate(self.columns):
                    col_my_width = col.get_my_width()

                    if col_my_width > max_cell_width:
                        cells_to_update = [(i, -1)]
                        max_cell_width = col_my_width

                    elif col_my_width == max_cell_width:
                        cells_to_update.append((i, -1))

                    for j, cell in enumerate(col.daughter_cells):
                        cell_width = cell.get_width()

                        if cell_width > max_cell_width:
                            cells_to_update = [(i, j)]
                            max_cell_width = cell_width

                        elif cell_width == max_cell_width:
                            cells_to_update.append((i, j))
                            

                for col_index, cell_index in cells_to_update:
                    if cell_index == -1:
                        self.columns[col_index].add_my_depth()
                    else:
                        d = self.columns[col_index].get_cell(cell_index).add_depth()

                current_total_width = self.get_current_width()
                print(current_total_width)
                if tries >= MAX_TRIES:
                    print("ERROR: Could not make table to desired width. Attempts tried: %d" % (tries))
                    break
            

    def get_current_width(self):
        borders = len(self.columns) + 1
        tally = 0
        for col in self.columns:
            tally += col.get_width()
        return borders + tally


    def show(self):
        # DEFINE CONSTANTS
        TOP_LEFT = '\u250C'
        TOP_RIGHT = '\u2510'
        BOTTOM_LEFT = '\u2514'
        BOTTOM_RIGHT = '\u2518'
        HORIZONTAL = '\u2500'
        VERTICAL = '\u2502'
        CROSS = '\u253C'

        TOP_PROTRUDE = '\u252C'  #(T)
        LEFT_PROTRUDE = '\u251C'
        RIGHT_PROTRUDE = '\u2524'
        BOTTOM_PROTRUDE = '\u2534'

        # print top line 
        print(TOP_LEFT, end='')
        for index, col in enumerate(self.columns):
            print(HORIZONTAL * col.get_width(), end='')
            if index + 1 == len(self.columns):
                print(TOP_RIGHT)
            else:
                print(TOP_PROTRUDE, end='')

        # max depth of the keys
        MAX_DEPTH = 0
        for col in self.columns:
            MAX_DEPTH = max(col.depth, MAX_DEPTH)

        # print the keys
        for index in range(MAX_DEPTH):
            for col in self.columns:
                print("{2}{1:^{0}}".format(col.get_width(), col.get_line(index), VERTICAL) , end="")
            print(VERTICAL)
        
        # print bottom of keys
        print(LEFT_PROTRUDE, end='')
        for index, col in enumerate(self.columns):
            print(HORIZONTAL * col.get_width(), end='')
            if index + 1 == len(self.columns):
                print(RIGHT_PROTRUDE)
            else:
                print(CROSS, end='')

        # loop over each row of each column now, printing out each line of each cell
        MAX_DAUGHTERS = 0
        for col in self.columns:
            MAX_DAUGHTERS = max(MAX_DAUGHTERS, col.get_total_daughters())

        for row in range(MAX_DAUGHTERS):
            # get maximum depth for row 1
            MAX_DEPTH = 0
            for col in self.columns:
                MAX_DEPTH = max(MAX_DEPTH, col.get_cell(row).get_depth())

            # print row "row"
            for depth in range(MAX_DEPTH):
                for col in self.columns:
                    print("{2}{1:^{0}}".format(col.get_width(), col.get_cell(row).get_line(depth), VERTICAL) , end="")
                print(VERTICAL)

            # line
            if row + 1 == MAX_DAUGHTERS:
                print(BOTTOM_LEFT, end='')
            else:
                print(LEFT_PROTRUDE, end='')
            for _index, _col in enumerate(self.columns):
                print(HORIZONTAL * _col.get_width(), end='')
                if _index + 1 == len(self.columns):
                    if row + 1 == MAX_DAUGHTERS:
                        print(BOTTOM_RIGHT)
                    else:
                        print(RIGHT_PROTRUDE)
                else:
                    if row + 1 == MAX_DAUGHTERS:
                        print(BOTTOM_PROTRUDE, end='')
                    else:
                        print(CROSS, end='')

    def show_csv(self):
        # print headers
        headers = []
        for col in self.columns:
            headers.append(col.text)
        print(",".join(headers))

        # print everything else
        MAX_DAUGHTERS = 0
        for col in self.columns:
            MAX_DAUGHTERS = max(MAX_DAUGHTERS, col.get_total_daughters())

        for row in range(MAX_DAUGHTERS):
            this_row = []
            for col in self.columns:
                try: 
                    this_row.append(col.get_cell(row).text)
                except:
                    this_row.append('')
            print(",".join(this_row))

    def show_json(self):
        items = []
        MAX_DAUGHTERS = 0
        for col in self.columns:
            MAX_DAUGHTERS = max(MAX_DAUGHTERS, col.get_total_daughters())

        """
        {
            items:[
                {"apple" : value, "orange": value1, ...}, # an item in items
                {"apple" : value2, "orange":value3, ...},... # order is broken
            ]
        }

        """

        for i in range(MAX_DAUGHTERS):
            item = {} # OrderedDict({}) is an alternative. This leaves OrderedDicts in the json output, which looks funny. Plus json doesn't need to be ordered anyways
            for col in self.columns:
                try:
                    item[col.text] = col.daughter_cells[i].text
                except:
                    item[col.text] = ""
            items.append(item)
        print({"items":items})

"""
if __name__ == "__main__":
    # example input
    data = OrderedDict([('apple', [40,50,60,70]), ('banana', [3,1,2]), ('orange', [200]), ('pear', [8,8,90,7])])
    t = Table(data, max_total_width=int(sys.argv[1]), fast_mode=False)
    t.show()
    t.show_csv()
    t.show_json()"""
