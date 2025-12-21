import json
import re
import traceback

spell_template_desc_md_path = 'templates/spell_template.md'
spell_template_footer_md_path = 'templates/spell_template.md'

class SpellBook():

    def __init__(self, spell_data_path):
        self.spells = {}
        self.load_spells(spell_data_path)
        self.spell_template_desc_md = open(spell_template_desc_md_path, 'r').read()
        self.spell_template_footer_md = open(spell_template_footer_md_path, 'r').read()


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
    

    def get_spell_embed_dict(self, name):
        embed_dict = {}
        spell = self.get_spell(name)
        if spell == "Spell not found.":
            return spell
        try:
            embed_dict["title"] = spell.get("name")

            embed_dict["color"] = self.get_school_color(spell.get("school"))

            embed_dict["description"] = self._get_spell_description_md(spell)

            if "entriesHigherLevel" in spell:
                fields["upcast"] = "\n**Upcast**: " + "\n".join(spell.get("entriesHigherLevel")[0].get("entries"))
            else:
                fields["upcast"] = ""

            embed_dict["footer"] = {"text": self.spell_template_footer_md.replace("{{{page}}}", spell.get("page"))}

        except Exception as e:
            print(traceback.format_exc())
            return f"Error generating markdown for spell {name}: {str(e)}"
    

    def _get_spell_description_md(self, spell):
        desc_fields = {}
        desc_fields["level"] = spell.get("level")

        try:
            desc_fields["school"] = spell_school_mapping.get(spell.get("school"))

            if spell.get("time")[0].get("unit") in action_mapping.keys():
                desc_fields["casting_time"] = action_mapping[spell.get("time")[0].get("unit")]
            else:
                desc_fields["casting_time"] = f"{spell.get("time")[0].get("number")} {spell.get("time")[0].get("unit")}"
                if spell.get("time")[0].get("number") > 1:
                    desc_fields["casting_time"] += "s"
            if "condition" in spell.get("time")[0]:
                desc_fields["casting_time"] += f", ({spell.get("time")[0].get("condition")})"
            if "meta" in spell and "ritual" in spell.get("meta"):
                desc_fields["casting_time"] += " or **Ritual**"

            if spell.get("range").get("distance").get("type") == "self" or spell.get("range").get("type") == "emanation":
                desc_fields["range"] = "Self"
            elif spell.get("range").get("distance").get("type") == "touch":
                desc_fields["range"] = "Touch"
            else:
                dist = spell.get("range").get("distance")
                desc_fields["range"] = f"{dist.get("amount")} {dist.get("type")}".strip()
                if dist.get("amount") == 1 and desc_fields["range"][-1:] == "s":
                    desc_fields["range"] = desc_fields["range"][:-1]

            desc_fields["components"] = ", ".join(spell.get("components", {}).keys()).upper()
            if "components" in spell and "m" in spell.get("components"):
                if isinstance(spell.get("components").get("m"), dict):
                    spell["components"]["m"] = spell.get("components").get("m").get("text")
                desc_fields["components"] += f" ({spell.get("components").get("m")})"
            dur_info = spell.get("duration", [{}])[0]
            if dur_info.get("type") == "instant":
                desc_fields["duration"] = "Instantaneous"
            else:
                desc_fields["duration"] = f"{spell.get("duration")[0].get("duration").get("amount")} {spell.get("duration")[0].get("duration").get("type")}"
                desc_fields["duration"] += "s" if spell.get("duration")[0].get("duration").get("amount", 0) > 1 else ""
                if "concentration" in spell.get("duration")[0]:
                    desc_fields["duration"] = "Concentration, up to " + desc_fields["duration"]
            
            description_md = self.spell_template_desc_md
            for key, value in desc_fields.items():
                description_md = description_md.replace(f"{{{key}}}", str(value))
            return description_md
        
        except Exception as e:
            print(traceback.format_exc())
            return f"Error generating markdown description for spell {spell.get("name")}: {str(e)}"

    def _get_spell_data(self, entries):
        data_fields = []

        # TODO contine here
        for entry in entries:
            if isinstance(entry, dict):
                if "type" in entry and entry["type"] == "entries":
                    data_fields.extend(entry.get("entries", []))
                elif "type" in entry and entry["type"] == "entry":
                    data_fields.append(entry.get("entry", ""))

        return data_fields

    def get_school_color(self, school):
        school_colors = {
            "A": 0x5DADE2,      # Blue
            "C": 0xF39C12,      # Orange
            "D": 0xAED6F1,      # Light blue
            "E": 0xE91E63,      # Pink
            "V": 0xE74C3C,      # Red
            "I": 0x9B59B6,      # Purple
            "N": 0x2C3E50,      # Dark gray
            "T": 0x27AE60,      # Green
        }
        return school_colors.get(school)

        
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