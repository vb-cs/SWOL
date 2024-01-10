import json
import os
import sys
import pandas as pd

file_path = sys.argv[0]


class Data:
    df = pd.DataFrame()

    @classmethod
    def load(cls, file_name):
        cls.df = pd.read_csv(file_name, header=[0, 1], index_col=0)

    @classmethod
    def exercises(cls):
        return cls.df.columns.get_level_values(0).unique()

    @classmethod
    def dates(cls):
        return cls.df.index

    @classmethod
    def merge(cls, df_to_merge: pd.MultiIndex):
        cls.df = (
            df_to_merge
            if cls.df.empty
            else cls.df.reset_index()
            .merge(df_to_merge.reset_index(), how="outer")
            .set_index("index")
        )

    @classmethod
    def save(cls):
        with open(os.path.abspath(f"{file_path}/../data/data.json"), "w") as data_file:
            json.dump(Data.data, data_file)

    @classmethod
    def add(cls, entry, name, date):
        # print(entry)
        if name in Data.data["exercises"]:
            Data.data["exercises"][name]["data"][date] = entry
            if entry["max_setn"] > Data.data["exercises"][name]["max_setn"]:
                Data.data["exercises"][name]["max_setn"] = entry["max_setn"]

        else:
            ex = {
                "max_setn": entry["max_setn"],
                "data": {date: entry},
            }
            Data.data["exercises"][name] = ex

    @classmethod
    def remove(cls, date):
        for ex in Data.data["exercises"].values():
            entry = ex["data"].pop(date, None)

            # replace max_setn if necessary
            if entry and entry["max_setn"] == ex["max_setn"]:
                ex["max_setn"] = max(ex["data"].values(), key=lambda e: e["max_setn"])["max_setn"]
