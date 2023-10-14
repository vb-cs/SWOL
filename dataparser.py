import json


class Parser:
    def parse():
        with open("data.json") as data_file:
            Parser.data = json.load(data_file)
    def save():
        with open("data.json", 'w') as data_file: 
            json.dump(Parser.data, data_file)
