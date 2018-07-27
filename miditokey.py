import pygame, time, pygame.midi as mid
import pyautogui
import msvcrt
from image import DashImage
from text import Text
from key_setup import keys
from pygame.locals import *


#Screen size constants
SCREENWIDTH = 1040
SCREENHEIGHT = 240
FULLSCREEN = False

#Start Pygame

pygame.init()
mid.init()
FPS = 60.0
fpsClock  = pygame.time.Clock()

DS = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

pygame.display.set_caption('midi2key')

bg = DashImage("bg.png", 0.0, 0.0)

keyboard = ['']*88
bk = 0
black_keys = [0]*36

# Key setup
xpos = 0.0
count = 3
black_key_next = False
set_gap = False
threeset = True

for i in range(52):
  if black_key_next:
    keyboard[i+bk] = DashImage("blackkey.png", (xpos+-.5)*20.0, 0.0, True, 'press_key' + str(i))
    count += 1
    black_keys[bk] = i + bk
    bk += 1
    if (threeset and count >= 3) or (not threeset and count >= 2):
      set_gap = True

    black_key_next = False

  if not black_key_next:
    keyboard[i+bk] = DashImage("whitekey.png", xpos*20.0, 0.0, True, 'press_key' + str(i))
    xpos += 1.0

    if set_gap:
      set_gap = False
      count = 0
      threeset = not threeset

    else:
      black_key_next = True


# Get the keys from file
with open("keys.txt", "r") as k:
  keys = k.read()


def midi_in(in_id):
  print ("Who is there?")

  print(mid.get_device_info(in_id))
  input_mid = mid.Input(in_id)

  while mid.get_default_input_id() != -1:

    if input_mid.poll():

      while input_mid.poll():
        mkey = input_mid.read(1)[0][0]
        if mkey[0] == 144:
          press_key(mkey[1])
        elif mkey[0] == 128:
          release_key(mkey[1])


def press_key(key_id):
  pyautogui.keyDown(key_list[key_id])


def release_key(key_id):
  pyautogui.keyUp(key_list[key_id])


def check_exit_i(input_mid):
  if msvcrt.kbhit():
    if msvcrt.getwch() == "-":
      quit()


def check_exit():
  if msvcrt.kbhit():
    if msvcrt.getwch() == "-":
      quit()


def quit():
  pygame.midi.quit()
  pygame.quit()
  exit()


playing = True

key_list = keys.split(",")

in_id = mid.get_default_input_id()

if in_id != -1:
  input_mid = mid.Input(in_id, 40)

else:
  quit()


print ("Who is there?")

print(mid.get_device_info(in_id))


while playing:

  bg.draw(DS)

  for k in range(88):
    if k not in black_keys:
      keyboard[k].draw(DS)

  for k in range(88):
    if k in black_keys:
      keyboard[k].draw(DS)

  for event in pygame.event.get():
    if event.type == QUIT:
      input_mid.close()
      quit()

  if input_mid.poll():
    ins = input_mid.read(40)
    
    for i in range(len(ins)):
      mkey = ins[i][0]
      if mkey[0] == 144:
        print(mkey[1])
        if mkey[2] != 0:
          press_key(mkey[1])
        else:
          release_key(mkey[1])

      elif mkey[0] == 128:
        release_key(mkey[1])

    check_exit_i(input_mid)
  check_exit()

  mouseclicked = False
  pygame.display.update()
  fpsClock.tick(FPS)

quit()