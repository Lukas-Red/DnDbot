from math import sqrt
from random import randint
import re

import spell_parser

distribution_file_path = "configs/modnar_distribution.txt"

min_spell_lvl = 0
max_spell_lvl = 9
min_spell_weight = 0
max_spell_weight = 1000000

class Modnar:    
    def __init__(self):
        self._load_distribution()
        self.spellbook = spell_parser.get_instance("spellbook")

    def _load_distribution(self):
        data = open(distribution_file_path, 'r').read().splitlines()
        self.distribution = {int(line.split(":")[0]): int(line.split(":")[1]) for line in data}
    
    def write_distribution(self):
        try:
            file = open(distribution_file_path, 'w')
            for k, v in self.distribution.items():
                file.write(f"{k}:{v}\n")
            return "Success"
        except Exception as e:
            return f"Exception occured while writing to file: {e}"

    def get_average(self):
        weighted_sum = 0
        sum = 0
        for level, quant in self.distribution.items():
            weighted_sum += level * quant
            sum += quant
        return weighted_sum / sum

    def get_variance(self):
        average = self.get_average()
        variance_sum = 0
        sum = 0
        for level, quant in self.distribution.items():
            variance_sum += (level - average)**2 * quant
            sum += quant
        return variance_sum / sum
    
    def get_stats(self):
        total_weight = sum(val for val in self.distribution.values())
        stats_str = f"**Distribution values** (<spell_level> : <weight>):\n{self.distribution}\n\n"
        stats_str += "**Percentage breakdown**:\n"
        for key, value in self.distribution.items():
            stats_str += f"Level {key}: {100 * value / total_weight:.2f}%\n"
        stats_str += f"\n**Average spell level**: {self.get_average():.2f}"
        stats_str += f"\n**Standard deviation**: {self.get_standard_deviation():.2f}"
        return stats_str
    
    def get_standard_deviation(self):
        return sqrt(self.get_variance())
    
    def get_modnar_spell_embed(self):
        spells = self.spellbook.get_spells_query(level=self._get_random_level())
        spell_names = [name for name in spells.keys()]
        return self.spellbook.get_spell_embed_dict(spell_names[randint(0, len(spell_names) -1)])

    def _get_random_level(self):
        total_weight = sum(val for val in self.distribution.values())
        random_num = randint(0, total_weight - 1)
        for spell_lvl, weight in self.distribution.items():
            if weight > random_num:
                return spell_lvl
            random_num -= weight

    # expects format like: k1:v1, k2:v2, ....
    def set_distribution(self, input_string):
        new_values = {}
        input_string = str(input_string)
        input_string = re.sub(r"[^0-9,:]", "", input_string)
        try:
            for entry in input_string.split(","):
                key, value = entry.split(":", 1)
                key, value = int(key), int(value)
                if not min_spell_lvl <= key <= max_spell_lvl:
                    raise Exception(f"bad spell level key {key}")
                if not min_spell_weight <= value <= max_spell_weight:
                    raise Exception(f"bad spell level weight {value}")
                new_values[key] = value
            for key, value in new_values.items():
                self.distribution[key] = value
            return "Success"
        except Exception as e:
            return f"Unable to set distribution: {e}"
