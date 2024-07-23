import json
import re

class Process:
    def __init__(self):
        self.res = {}
        self.count = 0

        tests = [self.si, self.si_affiliated, self.metric, self.non_si, self.american]

        for test in tests:
            test()

        with open("res.json", "w") as f:
            f.write(json.dumps(self.res))

        self.reverse = {}

        count = 0
        longest = 0

        for key, value in self.res.items():
            for abbrev in value["abbrev"]:
                if not abbrev.isalpha():
                    continue

                self.reverse[abbrev.upper()] = self.reverse.get(abbrev.upper(), []) + [key]
                count += 1
                longest = max(longest, len(abbrev))

        print(count, longest)

        with open("reverse.json", "w") as f:
            f.write(json.dumps(self.reverse))

    def add(self, matches, change):
        for match in matches:
            if not match[change["abbrev"]]:
                continue

            if match[ change["name"] ] in self.res:
                if  match[change["abbrev"]]  not in self.res[match[change["name"] ]]["abbrev"]:
                    self.res[match[change["name"]] ]["abbrev"].append( match[change["abbrev"]] )
                continue

            self.res[match[change["name"]]] = {
                "abbrev": [match[change["abbrev"]]],
                "definition": match[change.get("definition")] if change.get("definition") else None
            }

    def si(self):
        with open("documents/si.txt", "r") as f:
            text = f.read()

        matches = re.findall("The (\w+) \((\w+)\) is (.+).", text)

        self.add(matches, {"name": 0, "abbrev": 1})


    def si_affiliated(self):
        with open("documents/si-affiliated.txt", "r") as f:
            text = f.read()

        matches = re.findall("^([^\u0009]+)\u0009([^\u0009]+)", text, flags=re.MULTILINE)

        self.add(matches, {"name": 0, "abbrev": 1})

    def metric(self):
        with open("documents/metric.txt", "r") as f:
            text = f.read()

        matches = re.findall("The (.+) \((.+)\).*(?:equal to|corresponding to) ([^\n\[]+)\.(?:\[.+\]|)+\n", text)

        self.add(matches, {"name": 0, "abbrev": 1, "definition": 2})

    def american(self):
        with open("documents/american.txt", "r") as f:
            text = f.read()

        matches = re.findall("^([^\u0009]*)\u0009([^\u0009]*)\u0009([^\u0009]*)\u0009([^\u0009]*)\u0009([^\u0009]*)\u0009", text, flags=re.MULTILINE)

        self.add(matches, {"name": 0, "abbrev": 1, "definition": 4})

    def non_si(self):
        with open("documents/non_si_units.txt", "r") as f:
            text = f.read()

        matches = re.findall("(.+): (.*)", text, flags=re.MULTILINE)

        self.add(matches, {"name": 0, "abbrev": 1})


Process()