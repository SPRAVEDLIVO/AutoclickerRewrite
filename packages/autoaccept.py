__name__ = "autoaccept"

import engine, pyautogui, threading

def init_module(self):
    self.mkdir("packages/images/")

@engine.locate_event("packages/images/acceptimage.png")
def accept_located(self, x, y):
    print(f"[AutoAccept] Found accept image on x={x}, y={y}")
    pyautogui.click(x, y)