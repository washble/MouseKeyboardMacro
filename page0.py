import multiprocessing
from pynput import mouse, keyboard  # pip install pynput,  #1.6.8 version because pyinstaller
from typing import Optional

from macro import Macro

# Only click
class Page:
    def __init__(self):
        self.macro = Macro()
        self.kb_controller = self.macro.get_mecro_keyboard_controller()
        self.ms_controller = self.macro.get_mecro_mouse_controller()

        self.index = 0
        
        # Write your progress sequence
        # progress => order: (func, params, fallback index)
        self.sequence = {
            0: (self.macro.mouse_left_click, (), 1),
            1: (self.macro.delay, (0.01,), 0)
        }
    
    def progress(self, stop_event: Optional[multiprocessing.Event] = None):
        self.index = 0
        while self.index < len(self.sequence) and not stop_event.is_set():
            cur_sequence = self.sequence[self.index]
            result = self.invoke(cur_sequence)
            
            # print(f"progress====> {self.index}")
            
            if not result:
                fallback_index = cur_sequence[2]
                self.index = fallback_index
                
                # print(f"fallback_index====> {self.index}")
            else:
                self.index += 1
        
    def invoke(self, sequence):
        func, params, fallback = sequence
        
        return func(*params)    # Unpack parameters to call the function

    def search_word(self, search_word):
        try:
            self.kb_controller.press(keyboard.Key.ctrl)
            self.kb_controller.press('f')
            self.kb_controller.release('f')
            self.kb_controller.release(keyboard.Key.ctrl)
            
            for char in search_word:
                self.kb_controller.press(char)
                self.kb_controller.release(char)
                
            self.kb_controller.press(keyboard.Key.enter)
            self.kb_controller.release(keyboard.Key.enter)
            
            return True
        except Exception as e:
            print(f'Error in {search_word} search_word: {e}')
            
            return False