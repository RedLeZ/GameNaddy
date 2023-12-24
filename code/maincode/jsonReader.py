import json

def LoadJson(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def UpdateJson(file_path, key, new_value):
    data = LoadJson(file_path)

    data[key] = new_value

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)