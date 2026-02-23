import keyboard
import time

# Sends 20 "key down" events in 0.1 second intervals, followed by a single
# "key up" event.
for i in range(5):
    time.sleep(2)
    keyboard.press_and_release(0x41)


