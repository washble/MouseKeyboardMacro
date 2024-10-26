import time
import multiprocessing
import sys
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
# import random
# import cv2  # pip install opencv-python
import pyautogui  # pip install PyAutoGUI

'''
pip install pyinstaller

[exe build]
- Just make exe -
> pyinstaller main.py

- Only One exe File -
> pyinstaller -F main.py
'''

kb_controller = keyboard.Controller()
ms_controller = mouse.Controller()
def mecro_event(stop_event):  
    while not stop_event.is_set():
        # kb_controller.press(keyboard.Key.space)
        # kb_controller.release(keyboard.Key.space)
        # time.sleep(2)
        
        # kb_controller.press(keyboard.Key.f5)
        # kb_controller.release(keyboard.Key.f5)
        # time.sleep(2.5 + random.random())
        
        ms_controller.press(mouse.Button.left)
        time.sleep(0.001)
        ms_controller.release(mouse.Button.left)
        # time.sleep(1.5)
        time.sleep(0.01)
        
        # kb_controller.press(keyboard.KeyCode.from_char('w'))

# Image Click Version
images = ["./1.png", "./2.png", "./3.png", "./4.png"]
fail_images = ["./1.png", "./2.png", "./3_f.png", "./3_f.png"]
def image_mecro_event(stop_event):
    while not stop_event.is_set():
        for num in range(len(images)):
            isFail = False
            while not stop_event.is_set():
                find_image_path = images[num] if not isFail else fail_images[num]
                result = image_check_screen_all(find_image_path)
                if(result):
                    pyautogui.moveTo(image_position_x, image_position_y)
                    # pyautogui.click(x=image_position_x, y=image_position_y)
                    # time.sleep(0.5)
                    
                    time.sleep(1)
                    ms_controller.press(mouse.Button.left)
                    time.sleep(0.02)
                    ms_controller.release(mouse.Button.left)
                    time.sleep(1)
                    break
                
                isFail = not isFail
        
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
            mecro_start()
    elif button == mouse.Button.right and pressed:
        if start_pressed:
            start_pressed = False
            mecro_pause()
        else:
            mecro_stop()
            listener_stop()
            exe_exit()

def mecro_start():
    global process, start_pressed
    if process is None or not process.is_alive():
        print("Starting to macro.")
        stop_event.clear()
        # process = multiprocessing.Process(target=mecro_event, args=(stop_event,))
        process = multiprocessing.Process(target=image_mecro_event, args=(stop_event,))
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
            
def image_check_screen_all(image):
    global image_position_x, image_position_y
    try:
        image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=0.95)
        return True
    except Exception as e:
        print(f'Error in {image} image_check: {e}')
        return False
            
def image_check_screen_range(image, screen_range):
    global image_position_x, image_position_y
    try:
        image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=0.95, region=screen_range)
        return True
    except Exception as e:
        print(f'Error in {image} image_check: {e}')
        return False

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
