import os
import re
from pathlib import Path
from typing import Optional

CACHE_PATH = './cache'
mem = {}

def fileLookup(key: str) -> Optional[str]:
  key = re.sub(r'[^a-z0-9A-Z]', '', key)
  path = os.path.join(CACHE_PATH, key)
  file = Path(path)
  if file.exists():
    return file.read_text()
  return None

def fileSetValue(key: str, value: str) -> None:
  key = re.sub(r'[^a-z0-9A-Z]', '', key)
  path = os.path.join(CACHE_PATH, key)
  with open(path, mode='w') as file:
    file.write(value)

def lookup_key(key: str) -> Optional[str]:
  key = re.sub(r'[^a-z0-9A-Z]', '', key)
  if key in mem: return mem[key]
  return fileLookup(key)

def set_value(key: str, value: str) -> None:
  key = re.sub(r'[^a-z0-9A-Z]', '', key)
  if key in mem: mem[key] = value
  fileSetValue(key, value)