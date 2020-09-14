import time, pynput, threading, pyautogui, json, os, engine
from functools import partial

__name__ = "recording"

curRecord = []
wait_time = 0
mouseController = pynput.mouse.Controller()
keyboardController = pynput.keyboard.Controller()

@engine.tray_button("Exit recording")
def exit_recording(self, i, j):
    self.show()
    stopListeners()

def add_sleep():
    global wait_time
    curRecord.append({"action": "sleep", "time": time.time() - wait_time})
    wait_time = time.time()

def on_click(x, y, button, pressed):
    add_sleep()
    if pressed:
        curRecord.append({"action": "mousePress", "name": button.name, "x": x, "y": y})
    else:
        curRecord.append({"action": "mouseRelease", "name": button.name, "x": x, "y": y})

def on_press(key, mode="Press"):
    add_sleep()
    if (hasattr(key, "value")):
        key = key.value
    else:
        key = key.char
    curRecord.append({"action": f"key{mode}", "key": str(key).replace("'", "")})

def on_release(key):
    on_press(key, "Release")

def stopListeners():
    if ("mouse_listener" in globals()):
        print("Recording finished.")
        mouse_listener.stop()
        key_listener.stop()

def record(self):
    global wait_time, key_listener, mouse_listener
    seconds = self.simpledialog_module.askfloat("Input", "Number of seconds", parent = self, minvalue = 0)
    if seconds is not None:
        mouse_listener = pynput.mouse.Listener(on_click=on_click)
        key_listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
        mouse_listener.setName("Mouse Listener")
        key_listener.setName("Keyboard Listener")
        mouse_listener.start()
        key_listener.start()
        wait_time = time.time()
        threading.Timer(seconds, stopListeners).start()

def play(self):
    repeats = self.simpledialog_module.askinteger("Input", "Number of repetitions", parent = self, minvalue = 0)
    repeats = 0 if repeats is None else repeats
    for _ in range(repeats):
        for d in curRecord:
            action = d["action"]
            if (action == "sleep"):
                time.sleep(d["time"])
            elif (action == "mousePress"):
                pyautogui.moveTo(d["x"], d["y"])
                mouseController.press(getattr(pynput.mouse.Button, d["name"]))
            elif (action == "mouseRelease"):
                pyautogui.moveTo(d["x"], d["y"])
                mouseController.release(getattr(pynput.mouse.Button, d["name"]))
            elif (action == "keyPress"):
                keyboardController.press(d["key"])
            elif (action == "keyRelease"):
                keyboardController.release(d["key"])

def toname(str: str) -> str:
    return f"packages/presets/{str}.json"

def save(self):
    file_name = self.simpledialog_module.askstring("Saver", "Enter file name")
    if file_name is not None:
        with open(toname(file_name), "w") as f:
            json.dump(curRecord, f)

def load(self):
    global curRecord
    file_name = self.simpledialog_module.askstring("Loader", "Enter file name")
    name = toname(file_name)
    if file_name is not None and os.path.exists(name):
        with open(toname(file_name), "r") as f:
            curRecord = json.load(f)

def clear():
    global curRecord
    curRecord = []

@engine.load_function("recording")
def init_module(self):
    self.mkdir("packages/presets/")
    record_button  = self.add_button("recording", text="Record", command = lambda: record(self), width = 10)
    play_button    = self.add_button("recording", text="Play", command = lambda: play(self), width = 10)
    save_button    = self.add_button("recording", text="Save", command = lambda: save(self), width = 10)
    load_button    = self.add_button("recording", text="Load", command = lambda: load(self), width = 10)
    clear_button   = self.add_button("recording", text="Clear", command = lambda: clear(), width = 10)
    display_button = self.add_button("recording", text="Display", command = lambda: print(curRecord), width = 10)
    record_button.pack()
    play_button.pack()
    save_button.pack()
    load_button.pack()
    clear_button.pack()
    display_button.pack()