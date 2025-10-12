import requests as re
import json

n = re.get('https://newsapi.org/v1/sources?apiKey=6ff68bb78238495aa13017d62e6eceae')
new = json.dumps(n.json(), indent=4)     # Just to get a better view of the json
news = n.json()

req = ['name', 'category', 'language', 'country', 'description', 'url']

for new in range(len(news['sources'])):
    for r in req:
        print(f'{r.upper()}: {news['sources'][new][r]}\n', end='')
    print('-'*40, end='\n')