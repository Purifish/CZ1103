'''
  Marble Game:
  
  The objective is to score 5 points by catching the green target with the white marble 5 times.
  7 seconds is given for each target spawn. Score will reset to 0 if 7 seconds has passed.
  The game consists of 2 maps, each with its own portal to the other. The target may spawn in either map.

  Time and Points Limit can be changed by changing scoreToWin and timeBtwSpawns
'''

from sense_hat import SenseHat
from random import randint
import time

b = (0,0,255)
w = (255,255,255)
r = (255,0,0)
g = (0,255,0)

sense = SenseHat()

board2 = [[r,r,r,r,b,r,r,r],
          [r,b,r,b,b,b,b,r],
          [r,b,r,r,r,r,b,r],
          [r,b,r,b,r,r,b,r],
          [b,b,r,b,b,b,b,r],
          [r,b,r,r,r,r,b,r],
          [r,b,b,b,r,b,b,r],
          [r,r,r,r,r,r,r,r]]
          
board1 = [[r,r,r,r,r,r,r,r],
          [r,b,b,r,b,b,b,r],
          [r,b,r,r,b,r,b,r],
          [r,b,b,b,b,r,r,r],
          [r,b,r,r,b,b,b,b],
          [r,b,b,r,r,r,b,r],
          [r,r,b,b,b,r,b,r],
          [r,r,r,r,b,r,r,r]]

board = board1[:]
boardMap = 1

def DisplayBoard(board_):
    board_1D = sum(board_,[])
    sense.set_pixels(board_1D)
    
def check_wall(x, y, new_x, new_y):
    if board[new_y][new_x] != r:
        return new_x, new_y
    elif board[new_y][x] != r:
        return x, new_y
    elif board[y][new_x] != r:
        return new_x, y
    else:
        return x, y
    
def move_marble(pitch,roll,x,y):
    global board
    global boardMap
    newX = x
    newY = y

    if 1 < pitch < 179:
        newX -= 1
        if newX < 0:
            newX = 7
            board = board1[:]
            boardMap = 1
    elif 359 > pitch > 179:
        newX += 1
        if newX > 7:
            newX = 0
            board = board2[:]
            boardMap = 2
    if 1 < roll < 179:
        newY += 1
        if newY > 7:
            newY = 0
            board = board2[:]
            boardMap = 2
    elif 359 > roll > 179:
        newY -= 1
        if newY < 0:
            newY = 7
            board = board1[:]
            boardMap = 1
            
    newX, newY = check_wall(x,y,newX,newY)
    return newX, newY

def generateTarget(x, y):
    targX = randint(1,6)
    targY = randint(1,6)
    targMap = randint(1,2)
    if targMap == boardMap:
      if board[targY][targX] != r and board[targY][targX] != w:#avoid collision
          if abs(x - targX) + abs(y - targY) >= 6: #ensure new target is distant
              return targX, targY, targMap
      for i in range(6):
          for j in range(6):
              targX += 1
              if targX > 6:
                  targX -= 6
              if board[targY][targX] != r and board[targY][targX] != w:
                  if abs(x - targX) + abs(y - targY) >= 6:
                      return targX, targY, targMap
          targY += 1
          if targY > 6:
              targY -= 6
          if board[targY][targX] != r and board[targY][targX] != w:
              if abs(x - targX) + abs(y - targY) >= 6:
                  return targX, targY, targMap
    else: #distance not taken into account if target spawns in other map
      brd = []
      if targMap == 1:
        brd = board1[:]
      else:
        brd = board2[:]
      if brd[targY][targX] != r:#avoid collision
          return targX, targY, targMap
      for i in range(6):
          for j in range(6):
              targX += 1
              if targX > 6:
                  targX -= 6
              if brd[targY][targX] != r:
                  return targX, targY, targMap
          targY += 1
          if targY > 6:
              targY -= 6
          if brd[targY][targX] != r:
              return targX, targY, targMap

    #print("failure, targX =", targX, "targetY =", targY, "targetmap = ", targMap)
    return generateTarget(x,y) #lazy bug-fixer, by right this should never be needed

score = 0
x,y = 1, 1 #default marble position
targX, targY, targMap = 6, 1, 1 #default target position
board[y][x] = w
board[targY][targX] = g
scoreToWin = 5 #defines score needed to win
timeBtwSpawns = 7 #defines max time between each spawn in seconds
DisplayBoard(board)

start = time.time()
while score < scoreToWin:

    pitch = sense.get_orientation()['pitch']
    roll = sense.get_orientation()['roll']
    board[y][x] = b
    x,y = move_marble(pitch,roll,x,y)
    board[y][x] = w
    
    if x == targX and y == targY and boardMap == targMap: #acquired target
        score += 1
        if score < 5:
            targX, targY, targMap = generateTarget(targX, targY)
            start = time.time()
    elif time.time() - start >= timeBtwSpawns: #time up before acquire target
        if targMap == boardMap:
          board[targY][targX] = b
        targX, targY, targMap = generateTarget(targX, targY)
        score = 0 #reset score to 0
        start = time.time()
    if targMap == boardMap:
              board[targY][targX] = g
    DisplayBoard(board)
    if targMap == boardMap:
              board[targY][targX] = b
    time.sleep(0.1)

time.sleep(0.25)
sense.show_message("Yay!!!")
