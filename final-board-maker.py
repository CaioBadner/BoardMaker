#################################
### RUN THIS TO FINISH THE BOARDS
#############################

import json
from os import path

filename = 'raw_data.json'
rawBoards = []

if path.isfile(filename) is False:
  raise Exception("File not found")
with open(filename) as fp:
  rawBoards = json.load(fp)



for board in rawBoards:
  if (board['ready'] == True):

    realSize = board['rows'] * board['columns']
    tiles = board['tiles']
    totalWords = 0
    tileCount = {}
    tilesStarting = [0] * realSize
    tilesUsed = [0] * realSize
    wordCount = [0] * realSize
    comboMoves = board['normalGuesses'].values()
    words = board['normalGuesses'].keys()

    for moves in comboMoves:
      for i in range(0, len(moves), 2):
        tileIndex = int(moves[i:i+2])
        if i == 0:
          tilesStarting[tileIndex] += 1
        tilesUsed[tileIndex] += 1

    boardValid = True
    for tile in tilesUsed:
      if tile == 0:
        boardValid = False

    if (boardValid == False):
      print("AVISO!!! Board n#" + str(newId) + " nao usa todos as letras")

    for word in words:
      wordCount[len(word)] += 1
      totalWords += 1

    
    filename = 'final_data.json'
    finalBoards = []
    
    if path.isfile(filename) is False:
      raise Exception("File not found")
    with open(filename) as fp:
      finalBoards = json.load(fp)
    
    newId = len(finalBoards) + 1

    newBoard = {
      'boardId' : newId,
      'language' : board['language'],
      'rows' : board['rows'],
      'columns' : board['columns'],
      'totalWords' : totalWords,
      'tiles' : board['tiles'],
      'wordCount' : wordCount,
      'normalGuesses' : board['normalGuesses'],
      'tilesStarting' : tilesStarting,
      'tilesUsed' : tilesUsed,
      'bonusGuesses' : board['bonusGuesses']
    }

    finalBoards.append(newBoard)
    
    with open(filename, 'w') as json_file:
        json.dump(finalBoards, json_file, 
                            indent=4,  
                            separators=(',',': '))
        
    print("Board n#" + str(newId) + " pronto para jogar")
