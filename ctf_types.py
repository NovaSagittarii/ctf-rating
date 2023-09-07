from typing import Dict, TypedDict, Optional

## event api

class EventDuration(TypedDict):
  hours: int
  days: int

class Organizer(TypedDict):
  id: int
  name: str

class Event(TypedDict):
  ctf_id: int
  ctftime_url: str
  description: str
  duration: EventDuration
  finish: str
  format: str
  format_id: int
  id: int
  is_votable_now: bool
  live_feed: str
  location: str
  logo: str
  onsite: bool
  organizers: 'list[Organizer]'
  participants: int
  public_votable: bool
  restrictions: str
  start: str
  title: str
  url: str
  weight: float

## results api

class EventScore(TypedDict):
  place: int
  points: float
  team_id: int

class EventResult(TypedDict):
  scores: 'list[EventScore]'
  time: str
  title: str

class EventResultDict(Dict[str, EventResult]):
  pass

## teams api

class RatingRecord(TypedDict):
  country_place: Optional[int]
  organizer_points: Optional[int]
  rating_place: Optional[int]
  rating_points: Optional[float]

class Team(TypedDict):
  academic: bool
  aliases: 'list[str]'
  country: str
  id: int
  logo: str
  name: str
  primary_alias: str
  rating: Dict[int, RatingRecord]