import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup


class ParsGitHub:
    def __init__(self, username):
        self.url = f'https://github.com/{username}?tab=overview&from=2023-10-01&to=2023-10-27'
        # url = f'https://github.com/DevMosh?tab=overview&from=2023-10-01&to=2023-10-27'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')


    # метод, который будет выводить
    def respone_calendar(self, today=False, yesterday=False):
        calendar = self.soup.find('table', class_="ContributionCalendar-grid js-calendar-graph-table").find('tbody')  # достаем таблицу
        calendar = calendar.find_all('tr', style='height: 11px')  # достаем все линии из таблицы

        dict_calendar_contributions = {}  # словарь в который будем добавлять дни
        for date in calendar:  # проходимся по линиям
            calendar_line = date.find_all('td', class_="ContributionCalendar-day")
            for line in calendar_line:  # проходимся по дням в линии
                dict_calendar_contributions[line['data-date']] = line.getText()[0:16]

        sorted_dates = sorted(dict_calendar_contributions.items())  # делаем сортировку по дням, чтобы даты в словаре шли по возрстанию
        dict_calendar_contributions = {}

        for i in sorted_dates:
            try:
                contributions = int(''.join(re.findall(r'\b\d+\b', i[1])))
            except ValueError:
                contributions = 0

            dict_calendar_contributions.update({i[0]: contributions})

        dict_need_to_days = []
        if today is True:
            dict_need_to_days.append(self.need_is_day(dict_calendar_contributions))
        if yesterday is True:
            dict_need_to_days.append(self.need_is_day(dict_calendar_contributions, need_is_day=1))

        if True not in [today, yesterday]:
            return dict_calendar_contributions
        else:
            return dict_need_to_days

    @staticmethod
    def need_is_day(dict_calendar_contributions, need_is_day=0):
        day = str(datetime.now() - timedelta(days=1))[0:10]
        key_value = (day, dict_calendar_contributions[day])
        return key_value





pars = ParsGitHub('DevMosh')
print(pars.respone_calendar(yesterday=True))