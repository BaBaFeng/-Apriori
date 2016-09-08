Apriori


```Python
data = [
    ["A", "B", "E"],
    ["B", "D"],
    ["B", "C"],
    ["A", "B", "D"],
    ["A", "C"],
    ["B", "C"],
    ["A", "C"],
    ["A", "B", "C", "E"],
    ["A", "B", "C"]
]
```

print

```
support----------------------------------------------------------------
{'E': 2}
{'B': 7}
{'A': 6}
{'C': 6}
{'D': 2}
{'A,D': 1}
{'C,E': 1}
{'B,C': 4}
{'B,E': 2}
{'B,D': 2}
{'A,B': 4}
{'A,C': 4}
{'A,E': 2}
{'B,C,E': 1}
{'A,B,E': 2}
{'A,C,E': 1}
{'A,B,C': 2}
{'A,B,D': 1}
{'A,B,C,E': 1}
confidence----------------------------------------------------------------
The rule is:
A --> E--B--C 0.16666666666666666
B --> E--A--C 0.14285714285714285
C --> E--B--A 0.16666666666666666
E --> B--A--C 0.5
A--B --> E--C 0.25
A--C --> E--B 0.25
A--E --> B--C 0.5
B--C --> E--A 0.25
B--E --> A--C 0.5
C--E --> A--B 1.0
A--B--C --> E 0.5
A--B--E --> C 0.5
A--C--E --> B 1.0
B--C--E --> A 1.0
The associative rule is:
C--E --> A--B : 1.0
A--C--E --> B : 1.0
B--C--E --> A : 1.0
```