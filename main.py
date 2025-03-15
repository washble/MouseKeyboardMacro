import multiprocessing
import sys
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller

'''
pip install pyinstaller

[exe build]
- Just make exe -
> pyinstaller main.py

- Only One exe File -
> pyinstaller -F main.py
'''

from page0 import Page
page = Page()

def macro_event(stop_event):
    page.progress(stop_event)

def macro_event_loop(stop_event):
    while not stop_event.is_set():
        page.progress(stop_event)
        
def on_click(x, y, button, pressed):
    global start_pressed, mouse_controll_lock
    
    if button == mouse.Button.middle and not start_pressed and pressed:
        mouse_controll_lock = not mouse_controll_lock
        print(f"Mouse Control is locked: {mouse_controll_lock}")
    
    if mouse_controll_lock:
        return
    
    if button == mouse.Button.left and pressed:
        if not start_pressed:
            start_pressed = True
            macro_start()
    elif button == mouse.Button.right and pressed:
        if start_pressed:
            start_pressed = False
            macro_pause()
        else:
            macro_stop()
            listener_stop()
            exe_exit()

def macro_start():
    global process, start_pressed
    if process is None or not process.is_alive():
        print("Starting to macro.")
        stop_event.clear()
        process = multiprocessing.Process(target=macro_event, args=(stop_event,))
        # process = multiprocessing.Process(target=macro_event_loop, args=(stop_event,))
        process.start()
            
def macro_pause():
    global process
    if process:
        print("Stopping the macro.")
        stop_event.set()
        process.join()
        process = None

def macro_stop():
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
        macro_start()

def on_release(key):
    global start_pressed
    if key == keyboard.Key.page_down:
        if start_pressed:
            start_pressed = False
            macro_pause()
        else:
            macro_stop()
            listener_stop()
            exe_exit()

if __name__ == "__main__":
    print("Version 1.0.0")
    
    multiprocessing.freeze_support() # need for pyinstall exe
    stop_event = multiprocessing.Event()
    
    process = None
    mouse_controll_lock = False
    start_pressed = False
    
    image_position_x = 0
    image_position_y = 0

    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    keyboard_listener.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()

    # Sample of sharing variables across processes
    # manager = multiprocessing.Manager()
    # start_pressed = manager.Value('b', False)   # 'b' indicates boolean type; this allows sharing variables across processes.