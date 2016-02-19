# pagerank
topic pagerank and naive pagerank

##specifics
input the graph data into the file like this:

```
0.8
4
0 1 2
0 1
0 2
1 0
2 3
3 2
```

* the first line show the β of the pagerank path
* the second line is the nodes of the graph
* the third line is the topic node of the graph (for naive graph you should input all the node)
* the other lines are the edges


### run:

```py
python pagerank.py data.txt
```

### todo:
[ ] make the graph start with 1
