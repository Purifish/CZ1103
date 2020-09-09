from sense_hat import SenseHat
import time

s = SenseHat()

G = (0, 255, 0)
Y = (255, 255, 0)
B = (0, 0, 255)
R = (255, 0, 0)
W = (255, 255, 255)
NTH = (0, 0, 0)
Pink = (255, 105, 180)

def displayLetter(s, letter, colour):
  for pix in letter:
    s.set_pixel(pix[0], pix[1], colour)
    time.sleep(0.1)#delay 100 ms before colouring next pixel

letterO = (
    (2,1),(3,1),(4,1),(5,1),
    (6,2),(6,3),(6,4),(6,5),
    (5,6),(4,6),(3,6),(2,6),
    (1,5),(1,4),(1,3),(1,2))
    
letterR = (
    (1,6),(1,5),(1,4),(1,3),(1,2),(1,1),
    (2,1),(3,1),(4,1),(5,1),(5,2),(5,3),
    (4,3),(3,3),(2,3),(3,4),(4,5),(5,6))

letterD = (
    (1,1),(2,1),(3,1),(4,1),(5,1),
    (6,2),(6,3),(6,4),(6,5),
    (5,6),(4,6),(3,6),(2,6),(1,6),
    (1,5),(1,4),(1,3),(1,2))
    
letterL = (
    (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
    (2,6),(3,6),(4,6),(5,6),(6,6))
    
message = [letterO, letterR, letterD, letterL, letterO]
time.sleep(1)

for i in range(len(message)):
  if i >= 3:
    displayLetter(s, message[i], R)
  else:
    displayLetter(s, message[i], G)
  s.clear()
