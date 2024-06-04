
import datetime, json
from dictionary_pt import DICTIONARY
from os import path
from utils import printBoard, isTileAvailable, isValidMove, addToComboMoves, makeTiles, ALL_MOVES

#basic variables
ready = False
rows = 4
columns = 4
realSize = rows * columns
wordMinLength = 4
wordMaxLength = 16

#leave tiles empty to generate multiple new random boards with random tiles
#tiles = []
#if tiles is filled out then he will only generate one board
tiles = ['E', 'X', 'E', 'N', 'I', 'A', 'I', 'O', 'H', 'C', 'B', 'F', 'I', 'T', 'O', 'O']

#This saves all the possible 'combos', or words that can be guessed from the board as a list of STRINGS
possibleCombos = []

#This will save all the moves that led to each combo, as a list of STRINGS 
#such as 01040807 - where each two chars represent the tiles from 00 to 15
possibleMoves = []

#And later both lists will be combined in this DICT, with the combos as keys and the moves as the values
possibleGuesses = {}

#this will be kept empty so that we can move some obscure guesses here
bonusGuesses = {}

# counter[0] = total word count, [1] = word count by starting letter, [2] = dead tree count
counter = [0, 0, 0]




###############################
### METHODS 
##############################



#This is the start of the generation 
def getPossibleGuesses ():
  comboMoves = ''
  combo = ''
  index = 0
  for start in range(realSize):
    index = start
    combo = tiles[start]
    comboMoves = addToComboMoves('', start)
    counter[1] = 0
    print("Procurando palavras com", tiles[index])
    for move in ALL_MOVES:
      if isValidMove(realSize, index, move):
        continueCombo(index + move, comboMoves, combo)
    print("Encontrei " + str(counter[1]) + " palavras")

#This is the recursive function that checks all the combos
def continueCombo(index, comboMoves, combo):
  #First it makes the move
  combo += tiles[index]
  comboMoves = addToComboMoves(comboMoves, index)
  
  #If the combo is too long then end it
  if len(combo) > wordMaxLength:
    return
  
  #if the combo is the minimum length then it's worth checking if the word is real
  if len(combo) >= wordMinLength:
    if combo not in possibleCombos and combo in DICTIONARY:
      possibleCombos.append(combo)
      possibleMoves.append(comboMoves)
      counter[1] += 1
      counter[0] += 1
      #print('Encontrei uma palavra do dicionario! ' + combo + ' - ' + comboMoves) 

  #this checks whether is worth pursuing this combination any further 
  validCombo = False
  for word in DICTIONARY:
    if word.startswith(combo):
      validCombo = True
      break
  if validCombo:
    for move in ALL_MOVES:
      if isTileAvailable(index + move, comboMoves) and isValidMove(realSize, index, move):
        continueCombo(index + move, comboMoves, combo)
  else:
    counter[2] += 1

      
def getBoardID():

  filename = 'raw_data.json'
  boardList = []

  if path.isfile(filename) is False:
    raise Exception("File not found")
  
  # Read JSON file
  with open(filename) as fp:
    boardList = json.load(fp)

  return len(boardList) + 1



def addToJson(newBoard):
  filename = 'raw_data.json'
  listObj = []
  # Check if file exists
  if path.isfile(filename) is False:
    raise Exception("File not found")
    # Read JSON file
  with open(filename) as fp:
    listObj = json.load(fp)
  
  listObj.append(newBoard)
  with open(filename, 'w') as json_file:
      json.dump(listObj, json_file, 
                          indent=4,  
                          separators=(',',': '))
      
def isValidBoard():
  tileUse = [False] * realSize
  for move in possibleMoves:
    for i in range(0, len(move), 2):
        tile = int(move[i:i+2])
        if tileUse[tile] == False:
          tileUse[tile] = True
        if (all(tileUse)):
          return True
  return False

        




##################################
# START OF MAIN SCRIPT 
##################################
if __name__ == '__main__':

  howManyBoardsToMake = 1
  makeRandom = False

  if(tiles == []):
    input = input("Quantos BOARDS devo gerar? ")
    if input.isdigit():
      makeRandom = True
      howManyBoardsToMake = int(input)
    else: print("Não entendi, vou fazer só 1")
      
  else: 
    print("Gerando 1 BOARD com TILES predeterminados")

  boardID = getBoardID()
  totalBoards = boardID + howManyBoardsToMake - 1

  while boardID <= totalBoards:

    
    #this generates a new random board if the LIST tiles wasn't predetermined
    if tiles == []:
      tiles = makeTiles(realSize)
    
    printBoard(tiles, boardID)

    timer = datetime.datetime.now()

    #this is what populates the possibleGuesses global dict with the answers
    getPossibleGuesses()
    #then this adds all the results to the possibleGuesses dict
    for combo, move in zip(possibleCombos, possibleMoves):
        possibleGuesses.update({combo: move})

    possibleGuesses = dict(sorted(possibleGuesses.items()))
    finalTimer = str(datetime.datetime.now() - timer)

    #this checks if we have a board with at least every tile being used in one guess
    if (isValidBoard()):
      
      print("Board aprovado - salvo em raw_data.json")
      #if it is valid we add to the database
      newBoard = {
          'id' : boardID,
          'language' : "PT",
          'rows' : rows,
          'columns' : columns,
          'tiles' : tiles,
          'normalGuesses' : possibleGuesses,
          'bonusGuesses' : bonusGuesses,
          'ready' : ready
        }
      addToJson(newBoard)

      print("Encontrei um total de", str(counter[0]), "palavras")
      print("Combinacoes abandonadas:", str(counter[2]))
      print(newBoard)
      #a timer to check how fast this whole thing is 
      print("BOARD # ", str(boardID), "demorou", finalTimer, "minutos")
      print("\n")

      #and add to the counter
      boardID += 1

    else:
      if makeRandom == True:
        print("BOARD reprovado! Vou deletar tudo e comecar de novo. ")
      else: 
        print("Os TILES fornecido não geram um tabuleiro válido")
        break
      print(finalTimer + " minutos jogados no lixo...")
      print(" -_- ")
    
##### here we restart all the global variables  
    tiles = []
    tileCount = {}
    possibleCombos = []
    possibleMoves = []
    possibleGuesses = {}
    counter = [0,0,0]
##################################





