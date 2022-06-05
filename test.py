from constants import *
position = (3,2)
chunk = (0,1)
mx = position[0]*CELLSIZE + chunk[0] * CHUNKSIZE
my = position[1]*CELLSIZE + chunk[1] * CHUNKSIZE
print(mx,my)