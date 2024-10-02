import time
import multiprocessing
import sys
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
import random

'''
pip install pyinstaller

[exe build]
- Just make exe -
> pyinstaller main.py

- Only One exe File -
> pyinstaller -F main.py
'''

def mecro_event(stop_event):
    # kb_controller = keyboard.Controller()
    ms_controller = mouse.Controller()
    while not stop_event.is_set():
        # kb_controller.press(keyboard.Key.space)
        # kb_controller.release(keyboard.Key.space)
        # time.sleep(2)
        
        # kb_controller.press(keyboard.Key.f5)
        # kb_controller.release(keyboard.Key.f5)
        # time.sleep(2.5 + random.random())
        
        ms_controller.press(mouse.Button.left)
        ms_controller.release(mouse.Button.left)
        # time.sleep(0.02)
        time.sleep(0.1)
        
        # kb_controller.press(keyboard.KeyCode.from_char('w'))

def on_click(x, y, button, pressed):
    global process, right_click_count, shift_pressed

    if shift_pressed:
        if button == mouse.Button.left and pressed:
            right_click_count = 0
            if process is None or not process.is_alive():
                print("Shift + Left button pressed. Starting to macro.")
                stop_event.clear()
                process = multiprocessing.Process(target=mecro_event, args=(stop_event,))
                process.start()
        elif button == mouse.Button.right and pressed:
            right_click_count += 1
            if right_click_count == 1:
                print("Shift + Right button pressed once. Stopping the macro.")
                if process:
                    stop_event.set()
                    process.join()
                    process = None
            elif right_click_count == 2:
                print("Shift + Right button pressed twice. Exiting the script.")
                if process:
                    stop_event.set()
                    process.join()
                listener.stop()
                keyboard_listener.stop()
                sys.exit()

def on_press(key):
    global shift_pressed
    if key == keyboard.Key.shift_l:
        shift_pressed = True

def on_release(key):
    global shift_pressed
    if key == keyboard.Key.shift_l:
        shift_pressed = False

if __name__ == "__main__":
    stop_event = multiprocessing.Event()
    process = None
    right_click_count = 0
    shift_pressed = False

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    listener = mouse.Listener(on_click=on_click)
    listener.start()

    listener.join()
    keyboard_listener.join()
