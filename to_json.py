# Convert the dictionary into a json file

with open("fetch_details.py") as f:
    exec(f.read())

import json

def dict_to_json_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

dict_to_json_file(details, "output.json")