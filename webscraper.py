import json
import os
import csv
import requests
from bs4 import BeautifulSoup

if not os.path.exists('References'):
    os.mkdir('References')

unit_list = ['Byleth (M)', 'Byleth (F)', 'Edelgard', 'Dimitri', 'Claude', 'Hubert', 'Ferdinand', 'Linhardt', 'Caspar',
             'Bernadetta', 'Dorothea', 'Petra', 'Dedue', 'Felix', 'Ashe', 'Sylvain', 'Mercedes', 'Annette', 'Ingrid',
             'Lorenz', 'Raphael', 'Ignatz', 'Lysithea', 'Marianne', 'Hilda', 'Leonie', 'Seteth', 'Flayn', 'Hanneman',
             'Manuela', 'Gilbert', 'Alois', 'Catherine', 'Shamir', 'Cyril', 'Jeritza', 'Yuri', 'Balthus', 'Constance',
             'Hapi']


def get_abilities():
    url = 'https://serenesforest.net/three-houses/miscellaneous/abilities/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tb = soup.find('table')
    table_rows = [element for element in tb.find_all_next('tr')]
    abilities = []
    del table_rows[0]
    for row in table_rows:
        columns = row.find_all_next('td')
        abilities.append({
            "Name": columns[1].text.replace('\u2019', "'"),
            "Description": columns[2].text.replace('\u2019', "'")
        })
    with open("References/Abilities.json", 'w') as outfile:
        json.dump(abilities, outfile, indent=2)


def get_unit_stats(unit_name: str):
    """
    base_stats_model = {
        'Gender': '',
        'Crest': '',
        'Personal Ability': '',
        'House': '',
        'Level': '',
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
        'Skills': {
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
            'Flying': ''
        },
        'Supports': [{}]
    }
    """

    base_stats = {}

    if 'Byleth' in unit_name:
        url_suffix = 'Byleth'
    elif 'Lorenz' in unit_name:
        url_suffix = unit_name + "_(Three_Houses)"
    else:
        url_suffix = unit_name
    url = 'https://fireemblemwiki.org/wiki/' + url_suffix
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get gender
    if 'Byleth' not in unit_name:
        t_rows = soup.find('table', attrs={'style': 'border-spacing: 0; align:center; '
                                                    'border-radius: 15px; '
                                                    '-moz-border-radius: 15px; '
                                                    '-webkit-border-radius: 15px; '
                                                    '-khtml-border-radius: 15px; '
                                                    '-icab-border-radius: 15px; '
                                                    '-o-border-radius: 15px;; '
                                                    'border:1px solid #b0b0b0; '
                                                    'background:#222222'}).tbody
        base_stats['Gender'] = t_rows.tr.td.p.get_text().strip('\n')
    else:
        if 'M' in unit_name:
            base_stats['Gender'] = 'Male'
        else:
            base_stats['Gender'] = 'Female'

    # Get base level
    base_level = soup.find_all('td', attrs={'style': 'border: 1px solid #b0b0b0; border-top-right-radius: 5px; '
                                                     '-moz-border-radius-topright: 5px; '
                                                     '-webkit-border-top-right-radius: 5px; '
                                                     '-khtml-border-top-right-radius: 5px; '
                                                     '-icab-border-top-right-radius: 5px; -o-border-top-right-radius: '
                                                     '5px; border-bottom-right-radius: 5px; '
                                                     '-moz-border-radius-bottomright: 5px; '
                                                     '-webkit-border-bottom-right-radius: 5px; '
                                                     '-khtml-border-bottom-right-radius: 5px; '
                                                     '-icab-border-bottom-right-radius: 5px; '
                                                     '-o-border-bottom-right-radius: 5px;; background: #232855'})[
        0].get_text().strip("\n")

    base_stats['Level'] = base_level

    # Get crest
    crest = soup.find_all('th', attrs={'style': 'border: 2px solid #b0b0b0; border-top-left-radius: 5px; '
                                                '-moz-border-radius-topleft: 5px; -webkit-border-top-left-radius: 5px; '
                                                '-khtml-border-top-left-radius: 5px; -icab-border-top-left-radius: '
                                                '5px; '
                                                '-o-border-top-left-radius: 5px; border-bottom-left-radius: 5px; '
                                                '-moz-border-radius-bottomleft: 5px; '
                                                '-webkit-border-bottom-left-radius: '
                                                '5px; -khtml-border-bottom-left-radius: 5px; '
                                                '-icab-border-bottom-left-radius: 5px; -o-border-bottom-left-radius: '
                                                '5px;; background: #232855'})[1].find_next_sibling('td')
    if crest.get_text() == '--\n':
        base_stats['Crest'] = "None"
    else:
        base_stats['Crest'] = [c['title'] for c in crest.find_all('a')]

    # Get personal ability
    ability = \
        soup.find_all(attrs={'style': 'border-spacing: 3px; background: transparent'})[0].tbody.find_all('tr')[
            1].find_all(
            'td')[1].find_all('a')[1]['title']
    base_stats['Personal Ability'] = ability

    # Get house
    with open('References/Houses.json', 'r') as f:
        houses = json.load(f)
        base_stats['House'] = houses[unit_name]

    # Find stat tables
    stat_tb = soup.find('table', attrs={'style': 'margin-left:auto; margin-right:auto; width: 260px;'}).tbody.tr.td
    tabs = stat_tb.find('div', attrs={'class': 'tabcontents'}).find_all('div', "tab_content")

    # Get base stats
    base_table = tabs[0].table.tbody.find_all('tr')
    stats = []
    for tr in base_table:
        for stat in tr.find_all('td'):
            stats.append(stat.get_text().strip('\n'))
    base_stats.update({
        'HP': stats[0],
        'Strength': stats[2],
        'Magic': stats[4],
        'Dexterity': stats[6],
        'Speed': stats[8],
        'Luck': stats[1],
        'Defense': stats[3],
        'Resistance': stats[5],
        'Charm': stats[7]
    })

    # Get growths
    growth_table = tabs[1].table.tbody.find_all('tr')
    growths = []
    for tr in growth_table:
        for growth in tr.find_all('td'):
            growths.append(growth.get_text().strip('%\n'))
    base_stats.update({
        'HP Growth': stats[0],
        'Strength Growth': stats[2],
        'Magic Growth': stats[4],
        'Dexterity Growth': stats[6],
        'Speed Growth': stats[8],
        'Luck Growth': stats[1],
        'Defense Growth': stats[3],
        'Resistance Growth': stats[5],
        'Charm Growth': stats[7]
    })

    # Get skill levels
    skills_table = soup.find('td', attrs={
        'style': 'border: 1px solid #b0b0b0; background: #232855'}).parent.find_all('td')

    # print(skills_table)
    # skills_table = unit_table.tr.find_all('td')[2].table.tbody.find_all('tr')[6].find_all('td')
    skills = [skill.get_text().strip('\n') for skill in skills_table]
    base_stats['Skills'] = {
        'Sword': skills[0],
        'Lance': skills[1],
        'Axe': skills[2],
        'Bow': skills[3],
        'Brawl': skills[4],
        'Reason': skills[5],
        'Faith': skills[6],
        'Authority': skills[7],
        'Heavy Armor': skills[8],
        'Riding': skills[9],
        'Flying': skills[10]
    }

    # Get supports
    with open('References/Supports.json', 'r') as f:
        supports = json.load(f)
        base_stats['Supports'] = supports[unit_name]
    return base_stats


def get_supports_from_csv():
    support_dict = {}
    with open('References/FE3H Support Chart - Support.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        columns = []
        line_number = 0
        for row in csv_reader:
            if line_number == 0:
                columns = row[:-2]
                line_number += 1
                continue
            unit = row[0]
            supports = []
            for index, item in enumerate(row[1:-2]):
                if item == '':
                    continue
                support = {
                    "Unit": columns[index + 1],
                    "Max Rank": item
                }
                supports.append(support)
                support_dict[unit] = supports
            line_number += 1
    with open('References/Supports_csv.json', 'w') as outfile:
        json.dump(support_dict, outfile, indent=2)


def compile_unit_stats():
    units = {}
    for unit in unit_list:
        print("Generating " + unit + " stats...")
        units[unit] = get_unit_stats(unit)
    with open("References/Units.json", 'w') as outfile:
        json.dump(units, outfile, indent=2)


if __name__ == "__main__":
    compile_unit_stats()
    pass
