import requests
import re
import json

def parse_data(data):
    # Split the data into individual entries using regex
    entries = re.split(r'\n\n\n', data)

    parsed_data = {}
    for entry in entries:
        # Extract the title from the entry using regex
        title_match = re.search(r'title={(.+?)}', entry)
        if title_match:
            title = title_match.group(1)

            # Remove special characters from the title
            title = re.sub(r'[{}\\]', '', title)

            # Remove spaces and convert to lowercase for the key
            key = title.replace(' ', '_').lower()

            parsed_data[key] = entry

    return json.dumps(parsed_data, indent=4)

query = 'Physical Geography'
url = f'http://libris.kb.se/xsearch?query={query}&format=bibtex&n=50'

response = requests.get(url)
parse_data(response.text)
print(response.text)
t = response.text
tr = t.replace('\n\n\n', '\n')
tr.split('\n@')
print(tr)

# TODO: Hämta bibtext istället och parsa enligt följande
for entry in tr.split('\n@'):
    if not entry:
        continue
    # break
    title = re.findall(r'title={([^}]+)}', entry)[0]
    

data = response.json()
data_list = data['xsearch']['list']

ignore = {'urls', 'VtiD'}
parsed_data = {}
title = data_list[0].get('title')
if title in parsed_data:
    data_list[0].update({'title':f'{title}_dup'})
    title = data_list[0].get('title')

parsed_data.update({title:{k: v for k, v in data_list[0].items() if k not in ignore | {'title'}}})
