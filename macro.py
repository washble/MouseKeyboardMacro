from typing import Optional
import os
import time
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
import pyautogui  # pip install PyAutoGUI

class Macro:
    def __init__(self):
        self._kb_controller = keyboard.Controller()
        self._ms_controller = mouse.Controller()
        
    def get_mecro_keyboard_controller(self):
        return self._kb_controller
    
    def get_mecro_mouse_controller(self):
        return self._ms_controller
    
    def delay(self, sec):  # time: sec
        time.sleep(sec)
        
        return True
        
    def image_check_screen_all(self, image):
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(os.path.abspath(image), confidence=0.95)
            
            return (True, image_position_x, image_position_y)
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return (False, 0, 0)
                
    def image_check_screen_range(self, image, screen_range):
        global image_position_x, image_position_y
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(os.path.abspath(image), confidence=0.95, region=screen_range)
            
            return (True, image_position_x, image_position_y)
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return (False, 0, 0)
        
    def image_click_in_screen_all(self, image):
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(os.path.abspath(image), confidence=0.95)
            pyautogui.moveTo(image_position_x, image_position_y)
            self._ms_controller.press(mouse.Button.left)
            time.sleep(0.02)
            self._ms_controller.release(mouse.Button.left)
            
            return True
        except Exception as e:
            print(f'Error in {image} image_click: {e}')
            
            return False
        
    def mouse_left_click(self):
        self._ms_controller.press(mouse.Button.left)
        time.sleep(0.02)
        self._ms_controller.release(mouse.Button.left)