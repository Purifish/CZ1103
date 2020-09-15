'''
SenseHat Snake-playing AI Program by:
Muqaffa Al-Afham Bin Kamaruzaman
In this program, an AI plays the traditional Snake game. The basic MiniMax algorithm
is implemented, enhanced with Alpha-Beta pruning. Depending on the length of the snake,
the AI sees 7 to 32 moves ahead. The AI follows these instructions to the best of its abilities,
with the first having higher priority:
1. Don't die
2. Get to food asap
'''

from sense_hat import SenseHat
from random import randint
import time

s = SenseHat()

g = G = (0, 255, 0)
Y = (255, 255, 0)
B = (0, 0, 255)
r = R = (255, 0, 0)
W = (255, 255, 255)
n = O = (0, 0, 0)
Pink = (255, 105, 180)

directions = ['w','a','s','d'] #up, left, down, right
foodStart = (1,6)
baseDepth = 7
delay = 0.17
maxTime = 120
foodX, foodY = randint(0,1), randint(0,1)#generate random corner for food starting position
food = (foodStart[foodX],foodStart[foodY])

def moveRight(snake, growing): #move snake to the right
  tail = len(snake) - 1
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head will move
  
  if not growing:
    s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
    snake.pop()
  snake.insert(0, (snake[0][0]+1, snake[0][1]))
  s.set_pixel(snake[0][0], snake[0][1], Y) #colour new head
  return snake
  
def moveLeft(snake, growing):
  tail = len(snake) - 1
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head wil move
  
  if not growing:
    s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail 
    snake.pop()
  snake.insert(0, (snake[0][0]-1, snake[0][1]))
  s.set_pixel(snake[0][0], snake[0][1], Y) #colour new head
  return snake
  
def moveUp(snake, growing):
  tail = len(snake) - 1
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head wil move

  if not growing:
    s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
    snake.pop()
  snake.insert(0, (snake[0][0], snake[0][1]-1))
  s.set_pixel(snake[0][0], snake[0][1], Y) #colour new head
  return snake

def moveDown(snake, growing):
  tail = len(snake) - 1
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head will move

  if not growing:
    s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
    snake.pop()
  snake.insert(0, (snake[0][0], snake[0][1]+1))
  s.set_pixel(snake[0][0], snake[0][1], Y) #colour new head
  return snake
  
def generateFood(snake):
  fX = randint(1,6)
  fY = randint(1,6)

  if (fX,fY) in snake:
    for i in range(1,6):
      for j in range(1,6):
        fX += 1
        if fX > 6:
          fX -= 6
        if not ((fX,fY) in snake):
          return (fX,fY)
          
      fY += 1
      if fY > 6:
        fY -= 6
      if not ((fX,fY) in snake):
          return (fX,fY)
    return (0,0) #no space for food (snake is super long)
  else:
    return (fX,fY)
    
def GameOver(snake):
  if not (1 <= snake[0][0] <= 6) or not (1 <= snake[0][1] <= 6): #hit border
    return True
    
  body = snake[1:]
  if snake[0] in body: #hit own body
    return True
  return False
  
def Eval(snake, fd):
  if GameOver(snake):
    return -1000
  pureBody = snake[1:len(snake)-1] #body without head and tail
  hdUp = (snake[0][0], snake[0][1]-1)
  
  #this chain of if-blocks below check if all 3 moves kill the snake
  if hdUp in pureBody or hdUp[1] < 1:
    hdDown = (snake[0][0], snake[0][1]+1)
    if hdDown in pureBody or hdDown[1] > 6:
      hdLeft = (snake[0][0]-1, snake[0][1])
      if hdLeft in pureBody or hdLeft[0] < 1:
        hdRight = (snake[0][0]+1, snake[0][1])
        if hdRight in pureBody or hdRight[0] > 6:
          return -200
    
  if fd == (0,0):
    return 1000
  dist = abs(fd[0]-snake[0][0]) + abs(fd[1]-snake[0][1])
  return 1000 - dist * 5 #deduct points for every step snake has to take to reach food
    #this tells AI to go for the food
  
  
def Maxi(snake, fd, DIR, alpha, beta, initDepth, depth): #miniMax algo. AI aims to maximise points
  if GameOver(snake):
    return -1000 - depth * 10 # subtract depth so AI prolongs inevitable death instead of instant suicide
  if depth == 0:
    return Eval(snake, fd)
  if snake[0][0] == fd[0] and snake[0][1] == fd[1]: #if eating food, then remove food
    fd = (0,0)
    
  pen = 0
  if fd != (0,0): 
    pen = 1 #introduce 'penalty' for every move that does not eat food, encouraging AI to eat ASAP
  
  length = len(snake)
  temp = (snake[length-1][0], snake[length-1][1]) #temp stores the current tail of snake
  rightScore = leftScore = upScore = downScore = -10000
  
  for i in range(1):
    if DIR != 'a': #try move right, but only if direction is not left
      if not (snake[0][0]+1 == fd[0] and snake[0][1] == fd[1]): #if not eating
        snake.pop()
      snake.insert(0, (snake[0][0]+1, snake[0][1]))
      snakeTemp = snake[:] #copy a list before passing to function
      rightScore = Maxi(snakeTemp, fd, 'd', alpha, beta, initDepth, depth-1) - pen
      snake = snake[1:]
      if not (snake[0][0]+1 == fd[0] and snake[0][1] == fd[1]):
        snake.append(temp) #restore snake to what it was before moving right simulation
      
      if rightScore >= beta:
        break
      if rightScore > alpha:
        alpha = rightScore
  
    if DIR != 'd': #try move left, but only if direction is not right
      if not (snake[0][0]-1 == fd[0] and snake[0][1] == fd[1]):
        snake.pop()
      snake.insert(0, (snake[0][0]-1, snake[0][1]))
      snakeTemp = snake[:]
      leftScore = Maxi(snakeTemp, fd, 'a', alpha, beta, initDepth, depth-1) - pen
      snake = snake[1:]
      if not (snake[0][0]-1 == fd[0] and snake[0][1] == fd[1]):
        snake.append(temp) #restore snake to what it was before moving simulation 
      
      if leftScore >= beta:
        break
      if leftScore > alpha:
        alpha = leftScore
      
    if DIR != 's': #try move up, but only if direction is not down
      if not (snake[0][0] == fd[0] and snake[0][1]-1 == fd[1]):
        snake.pop()
      snake.insert(0, (snake[0][0], snake[0][1]-1))
      snakeTemp = snake[:]
      upScore = Maxi(snakeTemp, fd, 'w', alpha, beta, initDepth, depth-1) - pen
      snake = snake[1:]
      if not (snake[0][0] == fd[0] and snake[0][1]-1 == fd[1]):
        snake.append(temp) #restore snake to what it was before moving simulation 
      
      if upScore >= beta:
        break
      if upScore > alpha:
        alpha = upScore
      
    if DIR != 'w': #try move down, but only if direction is not up
      if not (snake[0][0] == fd[0] and snake[0][1]+1 == fd[1]):
        snake.pop()
      snake.insert(0, (snake[0][0], snake[0][1]+1))
      snakeTemp = snake[:]
      downScore = Maxi(snakeTemp, fd, 's', alpha, beta, initDepth, depth-1) - pen
      snake = snake[1:]
      if not (snake[0][0] == fd[0] and snake[0][1]+1 == fd[1]):
        snake.append(temp) #restore snake to what it was before moving simulation 
      
  score = max(rightScore,leftScore,upScore,downScore)
  if depth == initDepth:
    #print("rightS = %d\nleftS = %d\nupS = %d\ndownS = %d" % (rightScore,leftScore,upScore,downScore))
     #if score < 0:
        #input("")
    scoreList = [(rightScore,'d'),(leftScore,'a'),(upScore,'w'),(downScore,'s')]
    rNum = randint(0,3)#randomizes chosen move in case more than 1 move gives top score
    for i in range(rNum, rNum + 4):
      if score == scoreList[i % 4][0]:
        return scoreList[i % 4][1]
  return score
        
Border = [
          B, B, B, B, B, B, B, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, B, B, B, B, B, B, B]
          
loseScreen = [
              R, B, B, B, B, B, B, R,
              B, R, O, O, O, O, R, B,
              B, O, R, O, O, R, O, B,
              B, O, O, R, R, O, O, B,
              B, O, O, R, R, O, O, B,
              B, O, R, O, O, R, O, B,
              B, R, O, O, O, O, R, B,
              R, B, B, B, B, B, B, R]
              

Snake = [(4,3),(3,3),(2,3),(1,3)] #snake default position
snakeTemp = Snake[:]
snakeDir = 'd' #snake default direction
grow = False

s.clear()
time.sleep(0.5)
s.set_pixels(Border)
time.sleep(0.5)

for i in range(len(Snake)): #display initial snake position
  if i == 0: s.set_pixel(Snake[i][0], Snake[i][1], Y)
  else: s.set_pixel(Snake[i][0], Snake[i][1], R)

s.set_pixel(food[0],food[1], G) #display initial food position

start = time.time()#start game clock

while True:
  if time.time() - start >= maxTime: #stop program after 120s
    s.clear()
    break
  
  grow = False
  snakeTemp = Snake[:]
  snakeLen = len(snakeTemp)
  if snakeLen < 6: maxDepth = baseDepth
  elif snakeLen < 11: maxDepth = baseDepth + 1
  elif snakeLen < 18: maxDepth = baseDepth + 2
  elif snakeLen < 27: maxDepth = baseDepth + 3
  elif snakeLen < 30: maxDepth = baseDepth + 8
  elif snakeLen < 33: maxDepth = baseDepth + 11
  else: maxDepth = baseDepth + 25
  
  evalStart = time.time()
  choices = Maxi(snakeTemp, food, snakeDir, -10000, 1000, maxDepth, maxDepth)
  while time.time() - evalStart < delay: #prevents snake from moving too fast
    pass
  ch = choices
  if ch == 'w' and snakeDir != 's': #choose to move up
    if Snake[0][0] == food[0] and Snake[0][1]-1 == food[1]:
      grow = True
    Snake = moveUp(Snake, grow)
    snakeDir = 'w'
  elif ch == 'a' and snakeDir != 'd':
    if Snake[0][0]-1 == food[0] and Snake[0][1] == food[1]:
      grow = True
    Snake = moveLeft(Snake, grow)
    snakeDir = 'a'
  elif ch == 's' and snakeDir != 'w':
    if Snake[0][0] == food[0] and Snake[0][1]+1 == food[1]:
      grow = True
    Snake = moveDown(Snake, grow)
    snakeDir = 's'
  elif ch == 'd' and snakeDir != 'a':
    if Snake[0][0]+1 == food[0] and Snake[0][1] == food[1]:
      grow = True
    Snake = moveRight(Snake, grow)
    snakeDir = 'd'
    
  if grow: #generate new food if old food just got eaten
    food = generateFood(Snake)
    if food != (0,0):#if this is true then there is no more space
      s.set_pixel(food[0],food[1], G)
    else:
      maxTime = 10
      start = time.time()
  
  if GameOver(Snake):
    s.set_pixels(loseScreen)
    break
