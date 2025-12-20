import json
import re

spell_template_md_path = 'templates/spell_template.md'

class SpellBook():

    def __init__(self, spell_data_path):
        self.spells = {}
        self.load_spells(spell_data_path)
        self.spell_template_md = open(spell_template_md_path, 'r').read()


    def load_spells(self, spell_data_path):
        with open(spell_data_path, 'r') as file:
            data = json.load(file)
            for spell in data["spell"]:
                self.add_spell(simplify_string(spell["name"]), spell)


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
        return results
        
        
    def list_spell_keys(self):
        return [s for s in self.spells]
    

    def list_spells(self):
        return [self.spells[s]["name"] for s in self.spells]
    

    def spell_to_markdown(self, name):
        spell = self.get_spell(name)
        if spell == "Spell not found.":
            return spell
        
        name = spell.get("name", "Unknown name")
        level = spell.get("level", "Unknown level")
        school = spell_school_mapping.get(spell.get("school"), "Unknown school")
        casting_time = ""
        if spell.get("time")[0]("unit") in action_mapping.keys():
            casting_time += action_mapping[spell.get("time")[0]("unit")]
        else:
            casting_time += f"{spell.get("time")[0]("number")} {spell.get("time")[0]("unit")}"
            if spell.get("time")[0]("unit") > 1:
                casting_time += "s"
        if 'condition' in spell.get("time")[0]:
            casting_time += f", ({spell.get("time")[0]("condition")})"
        if "meta" in spell and "ritual" in spell.get("meta"):
            casting_time += " or **Ritual**"
        
    
spell_school_mapping = {
    "A": "Abjuration",
    "C": "Conjuration",
    "D": "Divination",
    "E": "Enchantment",
    "V": "Evocation",
    "I": "Illusion",
    "N": "Necromancy",
    "T": "Transmutation"
}

action_mapping = {
    "action": "Action",
    "bonus": "Bonus Action",
    "reaction": "Reaction"
}




def simplify_string(input_string):
    # Remove special characters and convert to lowercase
    simplified = re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()
    return simplified