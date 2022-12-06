import json

from bs4 import BeautifulSoup
import requests


class Services:
    allowed_commands = ('Adduser', 'Removeuser', 'Whitelist')
    whitelist_file_name = 'whitelist.json'

    def __init__(self, url):
        self.url = url

    def get_user_name(self, text):
        data, err = self.check_text(text)
        data.pop(0)
        name = ' '.join(data)

        return name, err

    def check_text(self, text):
        data = text.split(" ")

        if data[0] in self.allowed_commands:
            return data, False

        return data, True

    def get_html(self):
        r = requests.get(self.url)

        return r.text

    def get_data_table(self):
        raw_html = self.get_html()
        soup = BeautifulSoup(raw_html, 'html.parser')

        table = []
        bosses_list = soup.select('div.ipsWidget_inner.ipsPad ul li')
        for boss in bosses_list:
            boss_status = boss.select('span')[0].text
            boss_data = boss.select('b')
            boss_name = boss_data[0].text
            table.append(
                f'{boss_name}     {(boss_data[1].text + "-" + boss_data[2].text) if not boss_status == "Alive" else boss_status}')

        return table

    def read_from_whitelist(self):
        with open(self.whitelist_file_name, 'r') as file:
            return json.load(file)

    def write_to_whitelist(self, new_data):
        with open(self.whitelist_file_name, 'w') as file:
            file.write(json.dumps(new_data))

    def check_in_whitelist(self, username):
        whitelist = self.read_from_whitelist()

        if username in whitelist:
            return whitelist, True

        return whitelist, False
