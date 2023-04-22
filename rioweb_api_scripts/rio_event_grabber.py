import requests

"""pull events from api"""

url = "https://projectrio-api-1.api.projectrio.app/events/?users_&username=MORI&limit_games=20"
event_list = []
pull = requests.get(url).json()
for event in pull.values():
    for event_num in event.values():
        event_list.append(event_num)


url_tag = "&events="
url = "https://projectrio-api-1.api.projectrio.app/plate_data/?tag=Normal&username=MORI&tag=ranked&users_as_pitcher=1&limit_games=1"

for event in event_list:
    url += url_tag + f'{event}'

pull2 = requests.get(url).json()
# print(pull2)

