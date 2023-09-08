import re
import requests
from typing import Optional, TypedDict

import lxml
import lxml.html
# from lxml.cssselect import CSSSelector
# from lxml.html import fromstring

from fetch import fetch_json

def fetchHtml(url: str) -> lxml.html.HtmlElement:
  headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-modified-since": "Fri, 27 Jan 2000 07:41:28 GMT",
    "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  }
  page = requests.get(url, headers=headers, timeout=1)
  # print(url)
  return lxml.html.fromstring(page.text)

def _extractId(text: str) -> Optional[int]:
  search = re.search(r'([0-9]+)', text)
  if search:
    return int(search.group(1))
  return None

def fetchScoreboard(base_url: str) -> 'tuple[int]':
  w = 0
  ids = []
  while True:
    data = fetch_json(f'{base_url}json/leaderboard/all/now-{w}.json')
    for record in data['data']['leaderboard']:
      ids.append(record['id'])
    w += 100
    if w > data['data']['total']: break
  return tuple(filter(lambda x: x is not None, ids))

class Challenge(TypedDict):
  name: str
  solved: 'list[int]'
def fetchChallenge(base_url: str, challenge_id: int) -> Optional[Challenge]:
  h = fetchHtml(f'{base_url}challenge-id-{challenge_id}.html')
  ids = (_extractId(e.attrib['href']) for e in h.cssselect("tr>td a"))
  titles = tuple(e.text for e in h.cssselect("div.category-name")) # should be one
  if len(titles) == 0: return None
  return {
    'name': titles[0].strip(),
    'solved': tuple(x for x in ids if x is not None),
  }

def fetchChallenges(base_url: str) -> 'list[Challenge]':
  challs_json = fetch_json(f'{base_url}json/challs.json')
  challs: 'list[Challenge]' = []
  for chall in challs_json['data']:
    id = chall['id']
    solvers = []
    for solver_index in range(0, chall['solves'], 10):
      solves_data = fetch_json(f'{base_url}json/solves/{id}/{solver_index}.json')
      for x in solves_data['data']['solves']:
        solvers.append(x['userId'])
    challs.append({
      'name': id,
      'solved': solvers,
    })
  return challs

# h = fetchHtml('https://2023.irisc.tf/challenge-id-1.html')
# print([e.attrib['href'] for e in h.cssselect("tr>td a")])

if __name__ == '__main__':
  base_url = 'https://hope.dicega.ng/'
  print(fetchScoreboard(base_url))
  # print(fetchChallenge(base_url, 1))