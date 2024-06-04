
import random, math, datetime, json
from alphabet import LETTERS
from os import path
from utils import printBoard, isValidMove, ALL_MOVES
from dictionary_pt import DICTIONARY

boardSize = 4

realSize = boardSize ** 2

tiles = []



targetWord = ""

def getRandomMoves(moves):
  newMoves = [0] * len(moves)
  newPos = 0
  for move in moves:
    newPos = math.floor(random.random() * len(moves))
    while newMoves[newPos] != 0:
      newPos += 1
      if newPos == len(moves):
        newPos = 0
    newMoves[newPos] = move
  return newMoves


def makeBoard(request = ""):
  print(realSize)
  if request == "":
    newTiles = []
    letterCode = 0
    for tile in range(realSize):
      letterCode = math.floor(random.random() * 500)
      newTiles.append(LETTERS[letterCode])
    return newTiles
  else:
    allDone = False
    letterDone = False
    while allDone == False: 
      newTiles = ['?'] * realSize
      usedTiles = []
      tile = math.floor(random.random() * realSize)
      newTiles[tile] = request[0]
      usedTiles.append(tile)
      print("comecei com a letra", request[0], "na posicao", tile)
      for letter in range(len(request) - 1):
        print("estou vendo a letra", request[letter + 1])
        letterDone = False
        for move in randomMoves:
          if isValidMove(realSize, tile, move):
            nextTile = tile + move
            if nextTile not in usedTiles:
              newTiles[nextTile] = request[letter + 1]
              usedTiles.append(nextTile)
              print("coloquei a letra", request[letter + 1], "na posicao", nextTile)
              tile = nextTile
              letterDone = True
              break
        if letterDone == False:
          print("não achei lugar para a letra", request[letter + 1], "infelizmente vou comecar de novo")
          allDone = False
          break
        else: 
          allDone = True
          
         

    for tile in range(len(newTiles)):
      if newTiles[tile] == '?':
        letterCode = math.floor(random.random() * 500)
        newTiles[tile] = LETTERS[letterCode]
    
    return newTiles
  
  

##################################
#####
##################################
randomMoves = getRandomMoves(ALL_MOVES)

print("Eu sei gerar tabuleiros de 4x4 para jogos de DueLango")
answer = input("Quer que eu plante alguma palavra em especial? (S/N) ")
request = ""
if answer == "S" or answer == "s":
  x = 3
  while x > 0:
    word = input("Digite uma palavra de até 16 letras: ").upper()
    if word not in DICTIONARY:
      x -= 1
      print(word, "não é uma palavra válida, tente novamente")
    else:
      request = word
      break

if request == "":
  print("Gerando um BOARD totalmente aleatório")
else:
  print("Gerando um BOARD que contém a palavra:", request)

tiles = makeBoard(request)
printBoard(tiles)
print(tiles)

