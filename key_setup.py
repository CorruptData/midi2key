import os, time, pygame, pygame.midi as mid
import msvcrt

note_names = "C C#D D#E F F#G G#A A#B "

k = open("keys.txt", "r")
keys = k.read().split(",")
k.close()

if len(keys) != 128:
  keys = [""]*128

def press_key(key_id):
  
  print("Press a key to bind.")
  timeout = time.time() + 5

  while time.time() < timeout:

    if msvcrt.kbhit():
      cha = msvcrt.getwch()
      if cha == str(cha):
        keys[key_id] = cha
        k = open("keys.txt", "w")
        p = ""
        for i in range(128):
          p += str(keys[i] + ",")
        k.write(p)

        k.close()

        note = note_names[(mkey[1]%12)*2:((mkey[1]%12)*2)+2] + str((int(mkey[1]/12))-1)
        print(note + " is now bound to " + cha + "\n")
        return

  print("Timed out\n")

if __name__ == "__main__":
  pygame.init()
  mid.init()
  
  setting = True
  in_id = mid.get_default_input_id()

  if in_id != -1:

    input_mid = mid.Input(in_id)
    input_mid.poll()
    print("\nPress a note, or press '-' to exit.")

    while mid.get_default_input_id() != -1:

      if input_mid.poll():
        mkey = input_mid.read(1)[0][0]

        if mkey[0] == 144:
          print(note_names[(mkey[1]%12)*2:((mkey[1]%12)*2)+2] + str((int(mkey[1]/12))-1))
          press_key(mkey[1])
          print("Press another note, or press '-' to exit.")
          input_mid.close()
          input_mid = mid.Input(in_id)

      if msvcrt.kbhit():
        if msvcrt.getwch() == "-":
          input_mid.close()
          pygame.midi.quit()
          pygame.quit()
          exit()

  else:
    print("No midi device detected.")
