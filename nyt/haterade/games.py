from bs4 import BeautifulSoup
import json
import requests
from dateutil.parser import parse


def get_wordle(date_string):
    url = 'https://www.nytimes.com/svc/wordle/v2/{0}.json'.format(date_string)
    request = requests.get(url)
    r = json.loads(request.text)
    return r['solution']

def get_connections(date_string):
    url = "https://www.nytimes.com/svc/connections/v2/{0}.json".format(date_string)
    request = requests.get(url)
    r = json.loads(request.text)

    return r['categories']

def get_strands(date_string):
    url = "https://www.nytimes.com/svc/strands/v2/{0}.json".format(date_string)
    request = requests.get(url)
    parsed = json.loads(request.text)

    keep = ['printDate', 'themeWords', 'spangram', 'clue']

    return dict(zip(keep, [parsed[k] for k in keep]))

def get_spelling_bee():
    url = 'https://nytimes.com/puzzles/spelling-bee/'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')

    div = soup.find('div', id='js-hook-pz-moment__game')
    script = div.find('script')
    payload = script.contents[0][18:]
    parsed = json.loads(payload)
    answers = parsed['today']['answers']
    ordered = list(sorted(answers))

    date = parse(parsed['today']['printDate'])

    return ordered, date

def get_sudoku():

    url = 'https://www.nytimes.com/puzzles/sudoku/hard'
    request = requests.get(url)
    soup = BeautifulSoup(request.text, 'html.parser')
    div = soup.find('div', id='js-hook-pz-moment__game')
    script = div.find('script')
    payload = script.contents[0][18:]
    parsed = json.loads(payload)

    date = parse(parsed['displayDate'])
    types = ['easy', 'medium', 'hard']

    answers = dict(zip(types, [parsed[t] for t in types]))

    return answers, date
