import json
import os
import sys

file_path = sys.argv[0]


class Parser:
    def parse():
        with open(os.path.abspath(f"{file_path}/../data/data.json")) as data_file:
            Parser.data = json.load(data_file)

    def save():
        with open(os.path.abspath(f"{file_path}/../data/data.json"), "w") as data_file:
            json.dump(Parser.data, data_file)

    def add(entry, name, date):
        # print(entry)
        if name in Parser.data["exercises"]:
            Parser.data["exercises"][name]["data"][date] = entry
            if entry["max_setn"] > Parser.data["exercises"][name]["max_setn"]:
                Parser.data["exercises"][name]["max_setn"] = entry["max_setn"]

        else:
            ex = {
                "max_setn": entry["max_setn"],
                "data": {date: entry},
            }
            Parser.data["exercises"][name] = ex

    def remove(date):
        for ex in Parser.data["exercises"].values():
            entry = ex["data"].pop(date, None)

            # replace max_setn if necessary
            if entry and entry["max_setn"] == ex["max_setn"]:
                ex["max_setn"] = max(ex["data"].values(), key=lambda e: e["max_setn"])["max_setn"]
