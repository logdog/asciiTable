# asciiTable
Generates table with ASCII characters. Alrogithm runs in O(N^2) time normally, but with fast mode turned on, the algorithm is O(N).

## Example Input
```
data = OrderedDict([('apple', [40,50,60,70]), ('banana', [3,1,2]), ('orange', [200]), ('pear', [8,8,90,7])])
t = Table(data, max_total_width=90, fast_mode=False)
```

## Example Output
```
t.show()
t.show_csv()
t.show_json()
```
