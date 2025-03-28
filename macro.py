import time
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
import pyautogui  # pip install PyAutoGUI
import cv2  # pip install opencv-python
import numpy as np
from typing import Optional

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
            
            return True
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return False
                    
    def image_check_screen_range(self, image, screen_range, confidence=0.95):
        try:
            image_position_x, image_position_y = pyautogui.locateCenterOnScreen(image, confidence=confidence, region=screen_range)
            
            return True
        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            
            return False
    
    # Perform high-accuracy image search
    def image_check_in_screenshot_all(self, image, threshold=0.95):
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
                
                return True

            return False

        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            return (False, 0, 0)
        
    # Perform high-accuracy image search within a specified screen range
    def image_check_in_screenshot_range(self, image, screen_range, threshold=0.95):
        try:
            template = cv2.imread(image)

            # Take a screenshot
            screenshot = pyautogui.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Crop the screenshot to the specified screen range
            # x: The x-coordinate of the top-left corner of the region to search
            # y: The y-coordinate of the top-left corner of the region to search
            # width: The width of the search region
            # height: The height of the search region
            x, y, width, height = screen_range
            cropped_screenshot = screenshot[y:y+height, x:x+width]

            # Image matching
            result = cv2.matchTemplate(cropped_screenshot, template, cv2.TM_CCOEFF_NORMED)
            matched_y_positions, matched_x_positions = np.where(result >= threshold)

            # If a matching position is found
            if len(matched_x_positions) > 0:
                # image_position_x = matched_x_positions[0] + x + template.shape[1] // 2
                # image_position_y = matched_y_positions[0] + y + template.shape[0] // 2
                # Calculate the center position directly
                image_position_x = matched_x_positions[0] + x + (template.shape[1] >> 1)  # Adjust for cropped area
                image_position_y = matched_y_positions[0] + y + (template.shape[0] >> 1)  # Adjust for cropped area
                
                return True

            return False

        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            return False
    
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
                time.sleep(0.01)
                self._ms_controller.release(mouse.Button.left)
                
                return True

            return False

        except Exception as e:
            print(f'Error in {image} image_check: {e}')
            return False

    def key_press_release(self, key: Optional[keyboard.Key] = None):
        try:
            self._kb_controller.press(key)
            time.sleep(0.01)
            self._kb_controller.release(key)

            return True
        except Exception as e:
            print(f'Error in {key} key_press_release: {e}')
            return False
        
    def mouse_left_click(self):
        self._ms_controller.press(mouse.Button.left)
        time.sleep(0.01)
        self._ms_controller.release(mouse.Button.left)