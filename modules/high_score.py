import shelve

scoreFile = shelve.open('score.txt')

def updateScore(self, newScore):
  if('score' in scoreFile):
    score = scoreFile['score']
    if(newScore not in score):
      score.insert(0, newScore)

    score.sort()
    ranking = score.index(newScore)
    ranking = len(score)-ranking
  else:
    score = [newScore]
    ranking = 1

  print(score)
  print(ranking)
  scoreFile['score'] = score
  return ranking

newScore = score
updateScore(newScore)