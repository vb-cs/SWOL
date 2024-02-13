import json
import os
import sys
import pandas as pd

file_path = sys.argv[0]


class Data:
    df = pd.DataFrame()

    @classmethod
    def load(cls, data_path=f"{file_path}/../data/data.csv"):
        if os.path.exists(data_path):
            cls.df = pd.read_csv(data_path, header=[0, 1], index_col=0)
    
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
    def remove(cls, date):
        cls.df = cls.df.drop(index=date)

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

