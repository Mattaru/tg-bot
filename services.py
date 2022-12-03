import json

from bs4 import BeautifulSoup
import requests


class Services:
    commands = ['Adduser', 'Removeuser', 'Whitelist']

    def __init__(self, url):
        self.url = url

    def get_user_name(self, text):
        data, err = self.check_text(text)
        data.pop(0)
        name = ' '.join(data)

        return name, err

    def check_text(self, text):
        data = list(text.split(" "))

        if data[0] in self.commands:
            return data, False

        return data, True

    def get_http(self):
        r = requests.get(self.url)

        return r.text

    def get_data_table(self):
        http = self.get_http()
        soup = BeautifulSoup(http, 'html.parser')

        items = []
        table = []
        li_count = 0

        for item in soup.select('div.ipsPad'):
            for i in item.select('li'):
                li_count = li_count + 1

                for str in i.select('b'):
                    text = str.text
                    items.append(text)

        for i in range(1, li_count):
            table.append(f'{items.pop(0)}     {items.pop(0)} - {items.pop(0)}')

        return table

    def read_file(self):
        data = None

        with open('whitelist.json', 'r') as file:
            data = json.load(file)

        return data

    def write_file(self, new_data):
        with open('whitelist.json', 'w') as file:
            f = json.dumps(new_data)
            file.write(f)

        return False

    def get_check_whitelist(self, user_full_name):
        whitelist = self.read_file()

        if user_full_name in whitelist:
            return whitelist, True

        return whitelist, False