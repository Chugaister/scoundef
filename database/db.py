from json import load

data = {}

with open("database/devdata.json", "r", encoding="utf-8") as file:
    data = load(file)

history = []

