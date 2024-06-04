from alphabet import LETTERS
import math, random

ALL_MOVES = (-5, -4, -3, -1, 1, 3, 4, 5)

def printBoard(tempTiles, boardID = 1) :
  print("Board #" + str(boardID))
  line = ""
  for i in range(len(tempTiles)):
    if (i % 4 == 0): 
      line += " | "
    line += tempTiles[i] + " "
    if (i % 4 == 3):
      print(line + "|") 
      line = ""

def makeTiles(realSize):
  newTiles = []
  letterCode = 0
  for tile in range(realSize):
    letterCode = math.floor(random.random() * len(LETTERS))
    newTiles.append(LETTERS[letterCode])
  return newTiles

def isValidMove(realSize, index, move):
  
  nextMove = index + move    
  if nextMove < 0:
    return False
  if nextMove >= realSize:
    return False
  if index % 4 == 0 and (move == 3 or move == -1 or move == -5):
    return False
  if index % 4 == 3 and (move == -3 or move == 1 or move == 5):
    return False
  return True

def isTileAvailable(index, comboMoves):
  for i in range(0,len(comboMoves),2):
    if index == int(comboMoves[i:i+2]):
      return False
  return True

def addToComboMoves(comboMoves, index):
  if index < 10:
    return comboMoves + '0' + str(index)
  else: 
    return comboMoves + str(index)
  