import pygame, time, pygame.midi as mid
import pyautogui
import msvcrt
from key_setup import keys
from pygame.locals import *

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
      input_mid.close()
      pygame.midi.quit()
      pygame.quit()
      exit()


def check_exit():
  if msvcrt.kbhit():
    if msvcrt.getwch() == "-":
      pygame.midi.quit()
      pygame.quit()
      exit()


pygame.init()
mid.init()

playing = True

key_list = keys.split(",")

while playing:

  in_id = mid.get_default_input_id()
  
  if in_id != -1:

    input_mid = mid.Input(in_id, 10)

    while mid.get_default_input_id() != -1 and playing:

      while input_mid.poll():
        mkey = input_mid.read(10)[0][0]
        if mkey[0] == 144:
          print(mkey[1])
          press_key(mkey[1])
        elif mkey[0] == 128:
          release_key(mkey[1])

      check_exit_i(input_mid)
  check_exit()