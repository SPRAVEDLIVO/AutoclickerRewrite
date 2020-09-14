__name__ = "autoaccept"

import engine, pyautogui, threading, pynput
mouseController = pynput.mouse.Controller()

@engine.load_function("autoaccept")
def init_module(self):
    self.mkdir("packages/images/")

@engine.locate_event("autoaccept", "packages/images/acceptimage.png", confidence=0.8)
def accept_located(self, x, y):
    print(f"[AutoAccept] Found accept image on x={x}, y={y}")
    mouseController.position = (x, y)
    mouseController.press(pynput.mouse.Button.left)
    mouseController.release(pynput.mouse.Button.left)