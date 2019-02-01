# asciiTable
Generates a command line table that doesn't wrap lines, allowing for clean output. Runs in three output modes:
1) Tabular Form ```t.show()```
2) CSV Form ```t.show_csv()```
3) JSON Form ```t.show_json()```

Alrogithm runs in O(N^2) time normally, but with fast mode turned on, the algorithm is O(N). The difference is the cell widths and heights are calculated for every data point normally, but with fast mode only the first row of data is considered and a chart is made.

The max_total_width flag is the size of your terminal window in characters. Typical values are from 80-160. If the value entered is 

## Example
```python3
from table import Table
from collections import OrderedDict

data = OrderedDict([('apple', [40,50,60,70]), ('banana', [3,1,2]), ('orange', [200]), ('pear', [8,8,90,7])])
t = Table(data, max_total_width=90, fast_mode=False)
t.show()
t.show_csv()
t.show_json()
```
#### Example Output
```python3
>>> t.show()
┌─────┬───┬───┬────┐
│apple│ban│ora│pear│
│     │ana│nge│    │
├─────┼───┼───┼────┤
│ 40  │ 3 │200│ 8  │
├─────┼───┼───┼────┤
│ 50  │ 1 │   │ 8  │
├─────┼───┼───┼────┤
│ 60  │ 2 │   │ 90 │
├─────┼───┼───┼────┤
│ 70  │   │   │ 7  │
└─────┴───┴───┴────┘

>>> t.show_csv()
apple,banana,orange,pear
40,3,200,8
50,1,,8
60,2,,90
70,,,7

>>> t.show_json()
{'items': [{'apple': '40', 'pear': '8', 'banana': '3', 'orange': '200'}, {'apple': '50', 'pear': '8', 'banana': '1', 'orange': ''}, {'apple': '60', 'pear': '90', 'banana': '2', 'orange': ''}, {'apple': '70', 'pear': '7', 'banana': '', 'orange': ''}]}
```
# colorformat
A stdout wrapper in python for displaying colored text into supported linux terminals. Any terminal running bash should respond to the colors. The colors passed in are defined as constants at the top of the file, along with the attributes and background. The reset flag just sets the stdout back to standard text after the line is flushed onto the terminal, so setting this flag to false would just make future print statements follow with the same formatting. Of course, you can just call `resetText()` to end the formatting.

This example prints `Example String` in green, bold, italic, underscored, and blinking text on a white background.

## Examples
```python3
import colorformat as cf
print( cf.setText("Example String", 
       color=cf.GREEN, 
       attr=[cf.BOLD, cf.ITALIC, cf.UNDERSCORE, cf.BLINK], 
       bg=cf.BG_WHITE, 
       reset=True) 
)
```

If you need more control in the colors and your terminal supports 256 colors (e.g. Xterm), you can use `setText256()` method. The following example prints all of the possible background colors to the terminal in a really cool pattern. This will give you an idea of what numbers (0-256) correlate to what color, because for some reason it's counterintuitive.
```python3
import colorformat as cf
text = ""
for i in range(257):
  text += cf.setText256("{0:^5}".format(str(i)), bg=i)
print(text)
```

There are also some quick methods for setting warning, errors, and success messsages.
```python3
import colorformat as cf
print( cf.setSuccess("Test 1 passed: moving on to next check"))
print( cf.setWarning("Warning: are you sure you want to continue? Y/N"))
print( cf.setError("Fatal Error: params out of range"))
```

At my old work I threw in an easter egg that would make all loading bars rainbow colored certain days of the year. It was implemented something like this:
```python3
message = "Happy Easter!"
for i, letter in enumerate(message):
  text += cf.setText(letter, col=cf.RAINBOW[i%len(cf.RAINBOW)], attr=[cf.BOLD])
print(text)
```
