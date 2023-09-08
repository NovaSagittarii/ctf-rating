from sklearn.linear_model import LogisticRegression

import scrape
from rating import adjust_rating

n = int(input())
standings = tuple(map(int, input().strip().split()))
m = int(input())
rating_system = tuple(tuple(round(float(x)) for x in input().strip().split()) for x in range(m))
rating_aperf = {}
for id, rating, aperf, contests in rating_system:
  # 176403 2936 2794.6262421868273 10
  rating_aperf[id] = aperf

# print(n, m, standings[:5], rating_system[:5])

TASKS = [
  (1, 'welcome/Sanity Check (695)'),
  (8, 'web/babystretchy (104)'),
  (6, 'web/babycsrf (56)'),
  (26, 'web/Feeling Tagged (8)'),
  (28, 'web/mokerview (3)'),
  (21, 'rf/monke (1)'),
]

base_url = 'https://hope.dicega.ng/'
scoreboard = scrape.fetchScoreboard(base_url)
e2t = {} # event to team id mapping

for i, id in enumerate(scoreboard):
  if i >= len(standings): break
  e2t[id] = standings[i]

# print(e2t)

# for id in range(1, 50):
#   # if id != 21: continue
#   challenge = scrape.fetchChallenge(base_url, id)
for challenge in scrape.fetchChallenges(base_url):
  if challenge is None: continue
  # print(challenge)
  name = challenge['name']
  solved = challenge['solved']

  print('\t'.join(str(x) for x in (name,)), end='\t')
  solved_set = set(solved)
  failed = tuple(x for x in scoreboard if x not in solved_set and x in e2t)

  # add some fake ppl so sklearn doesnt explode
  solved_aperf = (*(5*[3500]), *(rating_aperf[e2t[x]] if e2t[x] in rating_aperf else 800 for x in solved if x in e2t))
  failed_aperf = (*(5*[-10000]), *(rating_aperf[e2t[x]] if e2t[x] in rating_aperf else 800 for x in failed if x in e2t))
  solve_count = len(solved)
  # print()
  # print(solved)
  # print(solved_aperf)

  # def mean(data: 'list[float]') -> float:
  #   return sum(data)/len(data)
  # print(' '.join(str(round(x)) for x in (len(solved_aperf), mean(solved_aperf), min(solved_aperf), max(solved_aperf))))
  # print(' '.join(str(round(x)) for x in (len(failed_aperf), mean(failed_aperf), min(failed_aperf), max(failed_aperf))))
  # for x in solved_aperf:
  #   print('\t'.join(str(x) for x in (x, 1)))
  # for x in failed_aperf:
  #   print('\t'.join(str(x) for x in (x, 0)))
  # break

  predicted_difficulty_cache = dict()
  ub, lb = 10000, -10000
  while round(lb) < round(ub):
    m = (lb + ub) / 2
    if m not in predicted_difficulty_cache:
      predicted_difficulty = 0.0
      K = 1024
      for a_perf in solved_aperf:
        a_perf -= K
        predicted_difficulty += 1. / (1. + (6.0 ** ((m - a_perf) / 400)))
      for a_perf in failed_aperf:
        a_perf += K
        predicted_difficulty += 1. / (1. + (6.0 ** ((m - a_perf) / 400)))
      predicted_difficulty /= len(solved_aperf) + len(failed_aperf)
      predicted_difficulty_cache[m] = predicted_difficulty
    predicted_difficulty = predicted_difficulty_cache[m]
    if predicted_difficulty < 0.5: ub = m
    else: lb = m
  difficulty = round(lb)
  # difficulty = adjust_rating(lb, 19)

  regressionDifficulty = -1
  # try:
  if True:
    model = LogisticRegression(solver='liblinear', random_state=0)
    model_data_x = tuple((x,) for x in (*solved_aperf, *failed_aperf))
    model_data_y = (*(1 for x in solved_aperf), *(0 for x in failed_aperf))
    model.fit(model_data_x, model_data_y)
    # print(' '.join(f'{model.predict([[x]])[0]:.0f}' for x in range(0, 3000, 500)), end='\t')
    for x in range(-10000, 10000, 10):
      if model.predict([[x]])[0] >= 0.5:
        regressionDifficulty = x
        break
  # except:
  #   regressionDifficulty = 9999
  print('\t'.join(str(x) for x in (solve_count, difficulty, regressionDifficulty)))

