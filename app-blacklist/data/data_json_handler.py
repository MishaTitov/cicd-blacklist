import json

DATA_FILE = "data/blacklist.json"

def load_data():
    """
    Load data from json
    """
    with open(DATA_FILE, 'r') as file:
        return json.load(file)
    
def add_entry(person_data):
    blacklist = load_data()
    blacklist.append(person_data)
    save_data(blacklist)

def delete_entry(name):
    blacklist = load_data()
    person_to_delete = next((person for person in blacklist if person['name'].lower() == name.lower()), None)
    if person_to_delete:
        blacklist.remove(person_to_delete)
        save_data(blacklist)
    
def save_data(data):
    """
    Save data to json
    """
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)