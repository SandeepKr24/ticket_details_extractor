# Convert the dictionary into a json file

with open("fetch_details.py") as f:
    exec(f.read())

import json

# function to dump the dictionary created in the 'fetch_details.py' file into a json file
def dict_to_json_file(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)

# calling the above function
dict_to_json_file(details, "output.json")