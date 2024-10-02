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
        time.sleep(0.01)
        
        # kb_controller.press(keyboard.KeyCode.from_char('w'))

# unused function
def on_click(x, y, button, pressed):
    global start_pressed
    if button == mouse.Button.left and start_pressed and pressed:
        mecro_start()
    elif button == mouse.Button.right and pressed:
        if start_pressed:
            mecro_pause()
        else:
            mecro_stop()
            listener_stop()
            exe_exit()
            
def mecro_start():
    global process
    if process is None or not process.is_alive():
        print("Starting to macro.")
        stop_event.clear()
        process = multiprocessing.Process(target=mecro_event, args=(stop_event,))
        process.start()
        
def mecro_pause():
    global process
    if process:
        print("Stopping the macro.")
        stop_event.set()
        process.join()
        process = None

def mecro_stop():
    global process
    if process:
        stop_event.set()
        process.join()
        
def listener_stop():
    global mouse_listener, keyboard_listener
    if mouse_listener:
        mouse_listener.stop()
    if keyboard_listener:
        keyboard_listener.stop()
        
def exe_exit():
    print("Exiting the script.")
    sys.exit()
    
def on_press(key):
    global start_pressed
    if key == keyboard.Key.page_up:
        start_pressed = True
        mecro_start()

def on_release(key):
    global start_pressed
    if key == keyboard.Key.page_down:
        if start_pressed:
            start_pressed = False
            mecro_pause()
        else:
            mecro_stop()
            listener_stop()
            exe_exit()

if __name__ == "__main__":
    print("Version 1.0.0")
    
    multiprocessing.freeze_support() # need for pyinstall exe
    stop_event = multiprocessing.Event()
    process = None
    start_pressed = False

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    # mouse_listener.start()

    keyboard_listener.join()
    # mouse_listener.join()
