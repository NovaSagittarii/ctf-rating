from urllib.request import Request, urlopen
import json
from typing import Dict

import ctf_types as TYPES
import file_cache as CACHE
import rating as RATING

def fetch_json(url: str) -> dict:
  print(url)
  cached = CACHE.lookup_key(url)
  if cached is not None: data = json.loads(cached)
  else:
    headers = {'User-Agent': 'Mozilla/5.0'}
    # a header is required for ctftime api response for some reason
    req = Request(url=url, headers=headers)
    with urlopen(req) as response:
      data = json.load(response)
      CACHE.set_value(url, json.dumps(data))
  return data

def get_event(event_id: int) -> TYPES.Event:
  if event_id < 1: raise ValueError("ctftime event ids start at 1")
  return fetch_json(f"https://ctftime.org/api/v1/events/{event_id}/")

def get_results(year: int) -> TYPES.EventResultDict:
  if year < 2011: raise ValueError("No ctftime results before 2011")
  return fetch_json(f"https://ctftime.org/api/v1/results/{year}/")

def get_team(team_id: int) -> TYPES.Team:
  if team_id < 1: raise ValueError("ctftime team ids start at 1")
  return fetch_json(f"https://ctftime.org/api/v1/teams/{team_id}/")

if __name__ == '__main__':
  rating_system = RATING.RatingSystem()
  for year in range(2011, 2024):
    # print(year)
    # TODO: sort by time using event_result['time']
    for id, event_result in get_results(year).items():
      event = get_event(int(id))
      if event['weight'] <= 0: continue
      # print(year, id, event_result['title'])
      standings = tuple(str(x['team_id']) for x in sorted(event_result['scores'], key=lambda x: float(x['points']), reverse=True))
      if int(id) == 1706:
        print(len(standings))
        print(" ".join(standings))
        break
      
      contest_type = RATING.ContestType.CUSTOM # RATING.ContestType.AGC if event['weight'] else RATING.ContestType.UNRATED
      rating_system.update(standings=standings, contest_type=contest_type, weight=1+(event['weight']/100*0.5))
  ratings = {}
  for id in rating_system.past_performances.keys():
    ratings[id] = rating_system.calc_rating(id)
  i = 0
  # print(ratings.items())
  print(len(ratings.items()))
  for id, performance in sorted(ratings.items(), key=lambda x: x[1], reverse=True)[:]:
    a_perf = rating_system.calc_a_perf(id, RATING.ContestType.CUSTOM)
    event_count = rating_system.competition_count(id)
    if i < 50:
      team = get_team(int(id))
      print(team['primary_alias'], id, performance, a_perf, event_count)
    else:
      print(id, performance, a_perf, event_count) # , rating_system.past_performances[id]
    i += 1