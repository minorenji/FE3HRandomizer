import json

with open('References/Unitsbk.json', 'r') as f:
    base_stats = json.load(f)


class Unit:
    def __init__(self, name):
        self.current_stats = {
            'Level': 0,
            'HP': 0,
            'Strength': 0,
            'Magic': 0,
            'Dexterity': 0,
            'Speed': 0,
            'Luck': 0,
            'Defense': 0,
            'Resistance': 0,
            'Charm': 0,
            'HP Growth': 0,
            'Strength Growth': 0,
            'Magic Growth': 0,
            'Dexterity Growth': 0,
            'Speed Growth': 0,
            'Luck Growth': 0,
            'Defense Growth': 0,
            'Resistance Growth': 0,
            'Charm Growth': 0,
        }

        self.base_stats = {}
        for key in self.current_stats.keys():
            self.base_stats[key] = base_stats[name][key]
            self.current_stats[key] = self.base_stats[key]
        self.basic_info = {key: base_stats[name][key] for key in base_stats[name].keys() & {'Gender', 'Crest', 'House',
                                                                                            'Personal Ability'}}
        self.skills = {
            'Sword': '',
            'Lance': '',
            'Axe': '',
            'Bow': '',
            'Brawl': '',
            'Reason': '',
            'Faith': '',
            'Authority': '',
            'Heavy Armor': '',
            'Riding': '',
            'Flying': '',
        }

    def export_to_file(self, fp):
        with open(fp, 'w') as outfile:
            unit_data = {
                'Current Stats': self.current_stats,
                'Skills': self.skills
            }
            json.dump(unit_data, outfile)

    def load_from_file(self, fp):
        with open(fp, 'r') as f:
            unit_data = json.load(f)
            self.current_stats = unit_data['Skills']