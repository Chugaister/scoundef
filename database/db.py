from json import load

data = {}

with open("database/data.json", "r", encoding="utf-8") as file:
    data = load(file)

history = []

