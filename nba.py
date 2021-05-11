#!/usr/bin/env python3

import json
import requests
from bs4 import BeautifulSoup, element
from datetime import datetime, timedelta
from prettytable import PrettyTable


def get_web_data():
    # get the score data from the nba website
    today = datetime.today()
    date = today.strftime("%Y%m%d")
    res = requests.get('https://data.nba.net/prod/v2/{}/scoreboard.json'.format(date))
    json_object = json.loads(res.text)

    return json_object


def team_name():
    # get the NBA team names and Abbreviations
    res = requests.get('https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations')
    bs4_html = BeautifulSoup(res.text, "html.parser")
    table = bs4_html.find('table', {'class': 'wikitable sortable'})
    team_dict = dict()
    table_with_label = table.find_all('tr')
    for team in table_with_label:
        if team.find('a'):
            team_abbr = team.find('td').text.rstrip()
            team_full = team.find('a').text
            team_dict[team_abbr] = team_full
    return team_dict


def insert_sting_middle(str, word):
    return str[:2] + word + str[2:]


def get_daily_score():
    # get the score data from the nba website
    web = get_web_data()
    message = []

    date = []
    today = datetime.today()
    date = today.strftime("%Y%m%d")
    team_dict = team_name()

    # get the data of daily games
    for index, game in enumerate(web['games']):
        host = game['hTeam']
        visitor = game['vTeam']
        info = game['nugget']
        location = game['arena']
        start_time = game['startTimeUTC']
        utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        utc_time = datetime.strptime(start_time, utc_format)
        local_time = utc_time + timedelta(hours=-8)
        table = PrettyTable(['Team', 'W/L', 'Score'])

        # table.add_row([
        #     '({:>3}) {:^23}'.format(visitor['triCode'], team_dict[visitor['triCode']]),
        #     'W{}/L{}'.format(visitor['win'], visitor['loss']),
        #     'N/A' if not visitor['score'] else visitor['score']
        # ])
        # table.add_row([
        #     '({:>3}) {:^23}'.format(host['triCode'], team_dict[host['triCode']]),
        #     'W{}/L{}'.format(host['win'], host['loss']),
        #     'N/A' if not host['score'] else host['score']
        # ])


        message.append(str('({0}) {1} (W{2}/L{3}) - {4}'.format(visitor['triCode'], team_dict[visitor['triCode']], visitor['win'], visitor['loss'],
        'N/A' if not visitor['score'] else visotor['score'])))
        message.append(str('({0}) {1} (W{2}/L{3}) - {4}'.format(host['triCode'], team_dict[host['triCode']], host['win'], host['loss'],
        'N/A' if not host['score'] else host['score'])))


        message.append('Location: {}'.format(location['name']))
        message.append('Time: {}'.format(local_time.strftime('%Y/%m/%d %H:%M')))
        message.append('')
    return message

if __name__ == "__main__":

    print(str(get_daily_score()))
