# asciiTable
Generates table with ASCII characters.

# How to use
Execute the asciiTable.py with this simple command:
```
python3 asciiTable.py Dog Cat Banana Monkey Madness
```
```
-----------------------------------------
| Dog | Cat | Banana | Monkey | Madness |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
```
This table has headers of Dog, Cat, Banana, Monkey, and Madness.

### Optional Arguments
- rows: Specifies how many rows there are in the table (default=4).
- height: Specifies the height of each cell (default=2).

### Using Optional Arguments
This creates a table with six rows, and a cell height of three.
```
python3 asciiTable.py Dog Cat Banana Monkey Madness -r 6 -c 3
```
The \-r refers to the number of rows, and the \-c refers to the cell height.
```
-----------------------------------------
| Dog | Cat | Banana | Monkey | Madness |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
|     |     |        |        |         |
|     |     |        |        |         |
|     |     |        |        |         |
-----------------------------------------
```

### Future Development
- [ ] Add Titles
- [ ] Print to file
- [ ] Auto-fill data
- [ ] Add average functionality
- [ ] Add more customizablity
