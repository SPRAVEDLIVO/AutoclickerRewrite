import tkinter as tk
import pystray, classes
from functools import partial
from PIL import Image
from pystray import MenuItem
from tkinter import simpledialog

import engine, pyautogui, threading, os
tools = engine.ImportTools()

@engine.tray_button("Show", default=True)
def show(self, i, j):
    self.show()

class MainClass(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("240x220")
        self.tray_ico = Image.open("icon.ico")
        self.tools = tools
        self.tk_module = tk
        self.simpledialog_module = simpledialog
        engine.call_init(self)
        threading.Thread(target=self.iterate_locates, name="Locates").start()
        self.protocol("WM_DELETE_WINDOW", self.init_icon)
    def show(self):
        self.tray_icon.stop()
        self.after(0, self.deiconify)
    def mkdir(self, dirname):
        if (not os.path.exists(dirname)):
            os.mkdir(dirname)
    def init_icon(self):
        self.withdraw()
        menu = []
        for name, lst in engine.tray_buttons.items():
            menu.append(MenuItem(name, partial(lst[0], self), **lst[1]))
        self.tray_icon = pystray.Icon("AutoClicker", self.tray_ico, "AutoClicker", pystray.Menu(*menu))
        self.tray_icon.run()
    def iterate_locates(self):
        while True:
            for path, func in engine.locate_events.items():
                try:
                    located = pyautogui.locateOnScreen(path)
                    if located is not None:
                        center = pyautogui.center(located)
                        x, y = center.x, center.y
                        func(self, x, y)
                except:
                    pass
    def add_button(self, module_name, **kwargs):
        button_obj = classes.Button(**kwargs)
        engine.add_button(module_name, button_obj)
        return button_obj

root = MainClass()
root.mainloop()