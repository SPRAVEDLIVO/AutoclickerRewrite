import tkinter as tk
import pystray, classes, time
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
        #self.iconphoto(tk.PhotoImage(file="icon.png"))
        self.title("AutoClicker")
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
            for module, pathes in engine.locate_events.items():
                if (not engine.is_module_disabled(module)):
                    for path in pathes:
                        try:
                            located = pyautogui.locateOnScreen(path[0], confidence=path[2])
                            if located is not None:
                                center = pyautogui.center(located)
                                x, y = center.x, center.y

                                path[1](self, x, y)
                        except:
                            pass
            time.sleep(0.0001)
    def add_button(self, module_name, **kwargs):
        button_obj = classes.Button(**kwargs)
        engine.add_button(module_name, button_obj)
        return button_obj

root = MainClass()
root.mainloop()