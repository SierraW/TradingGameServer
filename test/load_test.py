import json


with open('../storage/custom_database_store.json', 'r') as f:
    data = json.load(f)
    print(data)