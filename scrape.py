import re
import requests
from typing import Optional, TypedDict

import lxml
import lxml.html
# from lxml.cssselect import CSSSelector
# from lxml.html import fromstring

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
  h = fetchHtml(f'{base_url}scoreboard.html')
  # print(h.text)
  ids = (_extractId(e.attrib['href']) for e in h.cssselect(".scoreboard a.scoreboard-team-name"))

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

# h = fetchHtml('https://2023.irisc.tf/challenge-id-1.html')
# print([e.attrib['href'] for e in h.cssselect("tr>td a")])

if __name__ == '__main__':
  base_url = 'https://2023.irisc.tf/'
  print(fetchScoreboard(base_url))
  # print(fetchChallenge(base_url, 1))