import requests
import os
import json
from bs4 import BeautifulSoup

if not os.path.exists('References'):
    os.mkdir('References')


def get_abilities():
    url = 'https://serenesforest.net/three-houses/miscellaneous/abilities/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tb = soup.find('table')
    table_rows = [element for element in tb.find_all_next('tr')]
    abilities = []
    del table_rows[0]
    print(table_rows)
    for row in table_rows:
        columns = row.find_all_next('td')
        abilities.append({
            "Name": columns[1].text,
            "Description": columns[2].text
        })
    with open("References/Abilities.json", 'w') as outfile:
        json.dump(abilities, outfile, indent=2)


def get_supports(unit_name: str):
    url = 'https://fireemblemwiki.org/wiki/List_of_supports_in_Fire_Emblem:_Three_Houses'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    t_rows = soup.find_all('tr')
    for tr in [tr for tr in t_rows if 'align' in tr.attrs]:
        if unit_name in tr.find_all('td')[0].get_text():
            print(tr)
        #print(tr.find_all('td'))
        pass


if __name__ == "__main__":
    get_supports('Byleth (M)')