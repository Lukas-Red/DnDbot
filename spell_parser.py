import json
import re


class SpellBook():

    def __init__(self, spell_data_path):
        self.spells = {}
        self.load_spells(spell_data_path)

    def add_spell(self, name, description):
        self.spells[name] = description

    def get_spell(self, name):
        return self.spells.get(simplify_string(name), "Spell not found.")
    

    def get_spells_query(self, **criteria):
        results = self.spells

        for key, value in criteria.items():

            if key == "level":
                if isinstance(value, tuple):
                    min_value, max_value = value
                    results = {k: v for k, v in results.items() if min_value <= v.get("level", 0) <= max_value}
                if isinstance(value, int):
                    results = {k: v for k, v in results.items() if v.get("level", 0) == value}
                if isinstance(value, list):
                    results = {k: v for k, v in results.items() if v.get("level", 0) in value}
                    
            if key == "school":
                if isinstance(value, str):
                    results = {k: v for k, v in results.items() if v.get("school", "").lower() == value.lower()}
                if isinstance(value, list):
                    results = {k: v for k, v in results.items() if v.get("school", "").lower() in [s.lower() for s in value]}
        
    def list_spell_keys(self):
        return [s for s in self.spells]
    
    def list_spells(self):
        return [self.spells[s]["name"] for s in self.spells]
    

    def load_spells(self, spell_data_path):

        with open(spell_data_path, 'r') as file:
            data = json.load(file)
            for spell in data["spell"]:
                self.add_spell(simplify_string(spell["name"]), spell)




def simplify_string(input_string):
    # Remove special characters and convert to lowercase
    simplified = re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()
    return simplified