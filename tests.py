
tiles = ['a','b','c','d','e','f']
tilesStart = [0] * len(tiles)
tilesUsed = [9,9,9,9,9,9]

zipTiles = zip(tiles, tilesStart, tilesUsed)
for tile, tileStart, tileUsed in zipTiles:
  print(tile, 'starts', tileStart, 'words and is used', tileUsed, 'times')