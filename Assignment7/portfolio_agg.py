import pandas as pd
import json

with open("data/portfolio_structure-1.json", "r") as file:
    data = json.load(file)


for position in data["positions"]:
    value = position["quantity"] * position["price"]
    print(value)

