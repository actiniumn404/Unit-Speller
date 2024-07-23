import functools
import json
import random
import sys

with open("reverse.json", "r") as f:
    data = json.loads(f.read())

with open("res.json", "r") as f:
    raw_data = json.loads(f.read())

query = " " + input(">>> ").upper().replace(" ", "")

@functools.lru_cache()
def recurse(n):
    if n <= 0:
        return []
    res = []
    for i in range(5):
        if query[n - i:n + 1] in data:
            res.append(recurse(n - i - 1) + [random.choice(data[query[n - i:n + 1]])])
    if not res:
        return []
    return res[-1]

res = recurse(len(query) - 1)

for unit in res:
    print(raw_data[unit]["abbrev"], "\t", unit)