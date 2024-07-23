import functools
import json
import random
import sys

with open("reverse.json", "r") as f:
    data = json.loads(f.read())

with open("res.json", "r") as f:
    raw_data = json.loads(f.read())

q = "".join(filter(lambda x: x.isalpha() or x == " ", input(">>> ").upper()))

@functools.lru_cache()
def recurse(query, n):
    if n <= 0:
        return []
    res = []
    for i in range(5):
        if n - i <= 0:
            continue
        if query[n - i:n + 1] in data:
            res.append(recurse(query, n - i - 1) + [random.choice(data[query[n - i:n + 1]])])
    if not res:
        return []
    return res[-1]

for word in q.split(" "):
    r = recurse(" " + word, len(word))

    for unit in r:
        print(raw_data[unit]["abbrev"], "\t", unit)

    print()