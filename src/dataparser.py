import json
import os
import sys 

file_path = sys.argv[0]

class Parser:
    def parse():
        with open(f"{file_path}/../../data/data.json") as data_file:
            Parser.data = json.load(data_file)

    def save():
        with open(f"{file_path}/../../data/data.json", "w") as data_file:
            json.dump(Parser.data, data_file)

    def add(entry, name, date, index):
        #print(entry)
        if index < len(Parser.data["exercises"]):
            Parser.data["exercises"][index]["data"][date] = entry
        else:
            ex = {
                "name": name,
                "max_nsets": 1,
                "data": {date: entry},
            }
            Parser.data["exercises"].append(ex)

        if entry["nsets"] > Parser.data["exercises"][index]["max_nsets"]:
            Parser.data["exercises"][index]["max_nsets"] = entry["nsets"]
        
        
    def remove(date):
        for ex in Parser.data["exercises"]:
            ex["data"].pop(date, None)
