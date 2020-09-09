from sense_hat import SenseHat
from random import randint
import time

s = SenseHat()

G = (0, 255, 0)
Y = (255, 255, 0)
B = (0, 0, 255)
R = (255, 0, 0)
W = (255, 255, 255)
O = (0, 0, 0)
Pink = (255, 105, 180)

directions = ['w','a','s','d'] #up, left, down, right
delay = 0.1

def moveRight(snake):
  
  time.sleep(delay)
  tail = len(snake) - 1
  s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head will move
  s.set_pixel(snake[0][0]+1, snake[0][1], Y) #colour new head
  snake.pop()
  snake.insert(0, (snake[0][0]+1, snake[0][1]))
  
  return snake
  
def moveLeft(snake):
  
  time.sleep(delay)
  tail = len(snake) - 1
  s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head wil move
  s.set_pixel(snake[0][0]-1, snake[0][1], Y) #colour new head
  snake.pop()
  snake.insert(0, (snake[0][0]-1, snake[0][1]))
  
  return snake
  
def moveUp(snake):
  
  time.sleep(delay)
  tail = len(snake) - 1
  s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head wil move
  s.set_pixel(snake[0][0], snake[0][1]-1, Y) #colour new head
  snake.pop()
  snake.insert(0, (snake[0][0], snake[0][1]-1))
  
  return snake

def moveDown(snake):
  
  time.sleep(delay)
  tail = len(snake) - 1
  s.set_pixel(snake[tail][0], snake[tail][1], O) #clear tail
  s.set_pixel(snake[0][0], snake[0][1], R) #recolour current head as head wil move
  s.set_pixel(snake[0][0], snake[0][1]+1, Y) #colour new head
  snake.pop()
  snake.insert(0, (snake[0][0], snake[0][1]+1))
  
  return snake

Border = [
          B, B, B, B, B, B, B, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, O, O, O, O, O, O, B,
          B, B, B, B, B, B, B, B]

Snake = [(4,3),(3,3),(2,3),(1,3)] #snake default position
snakeDir = 'd' #snake default direction

s.clear()
time.sleep(0.5)
s.set_pixels(Border)
time.sleep(0.5)

for i in range(len(Snake)): #display initial snake position
  if i == 0:
    s.set_pixel(Snake[i][0], Snake[i][1], Y)
  else:
    s.set_pixel(Snake[i][0], Snake[i][1], R)

start = time.time()
while True:
  
  ch = directions[randint(0,3)]
  if ch == 'w' and snakeDir != 's' and Snake[0][1] != 1:
    Snake = moveUp(Snake)
    snakeDir = 'w'
  elif ch == 'a' and snakeDir != 'd' and Snake[0][0] != 1:
    Snake = moveLeft(Snake)
    snakeDir = 'a'
  elif ch == 's' and snakeDir != 'w' and Snake[0][1] != 6: 
    Snake = moveDown(Snake)
    snakeDir = 's'
  elif ch == 'd' and snakeDir != 'a' and Snake[0][0] != 6:
    Snake = moveRight(Snake)
    snakeDir = 'd'
    
  if time.time() - start >= 20: #stop program after 10s. Remove this if block for forever loop
    s.clear()
    break
