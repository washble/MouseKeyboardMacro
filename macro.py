from typing import Optional
import os
import time
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
import pyautogui  # pip install PyAutoGUI
import cv2
import numpy as np

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

    # Perform simple image search
    def image_check_screen_all(self, image, confidence=0.95):
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            
            return (True, image_position_x, image_position_y)
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return (False, 0, 0)
    
    # Perform high-accuracy image search and click
    def image_click_in_screenshot_all(self, image, threshold=0.95):
        try:
            template = cv2.imread(image)

            # Take a screenshot
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Image matching
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            matched_y_positions, matched_x_positions = np.where(result >= threshold)

            # If a matching position is found
            if len(matched_x_positions) > 0:
                # image_position_x = matched_x_positions[0] + template.shape[1] // 2
                # image_position_y = matched_y_positions[0] + template.shape[0] // 2
                # Calculate the center position directly
                image_position_x = matched_x_positions[0] + (template.shape[1] >> 1)  # Using bitwise right shift for division by 2
                image_position_y = matched_y_positions[0] + (template.shape[0] >> 1)  # Using bitwise right shift for division by 2
                
                pyautogui.moveTo(image_position_x, image_position_y)
                self._ms_controller.press(mouse.Button.left)
                time.sleep(0.02)
                self._ms_controller.release(mouse.Button.left)
                
                return True

            return False

        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            return False
                
    def image_check_screen_range(self, image, screen_range, confidence=0.95):
        global image_position_x, image_position_y
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=confidence, region=screen_range)
            
            return (True, image_position_x, image_position_y)
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return (False, 0, 0)
    
    # Perform simple image search and click
    def image_click_in_screen_all(self, image, confidence=0.95):
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            pyautogui.moveTo(image_position_x, image_position_y)
            self._ms_controller.press(mouse.Button.left)
            time.sleep(0.02)
            self._ms_controller.release(mouse.Button.left)
            
            return True
        except Exception as e:
            print(f'Error in {image} image_click: {e}')
            
            return False
    
    # Perform high-accuracy image search and click
    def image_click_in_screenshot_all(self, image, threshold=0.95):
        try:
            template = cv2.imread(image)

            # Take a screenshot
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Image matching
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            matched_y_positions, matched_x_positions = np.where(result >= threshold)

            # If a matching position is found
            if len(matched_x_positions) > 0:
                # image_position_x = matched_x_positions[0] + template.shape[1] // 2
                # image_position_y = matched_y_positions[0] + template.shape[0] // 2
                # Calculate the center position directly
                image_position_x = matched_x_positions[0] + (template.shape[1] >> 1)  # Using bitwise right shift for division by 2
                image_position_y = matched_y_positions[0] + (template.shape[0] >> 1)  # Using bitwise right shift for division by 2
                
                pyautogui.moveTo(image_position_x, image_position_y)
                self._ms_controller.press(mouse.Button.left)
                time.sleep(0.02)
                self._ms_controller.release(mouse.Button.left)
                
                return True

            return False

        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            return False
        
    def mouse_left_click(self):
        self._ms_controller.press(mouse.Button.left)
        time.sleep(0.02)
        self._ms_controller.release(mouse.Button.left)