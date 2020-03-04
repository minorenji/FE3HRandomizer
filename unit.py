import json

with open('References/Units.json', 'r') as f:
    base_stats = json.load(f)


class Unit:
    def __init__(self, name, file_path=None):
        self.base_stats = base_stats[name]
        self.basic_info = {
            'Gender': self.base_stats['Gender'],
            'Crests': self.base_stats['Crest'],
            'House': self.base_stats['House'],
            'Personal Ability': self.base_stats['Personal Ability']
        }
        self.current_stats = {
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
        for key in self.current_stats.keys():
            self.current_stats[key] = self.base_stats[key]
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