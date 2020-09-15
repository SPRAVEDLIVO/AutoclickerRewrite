import os, importlib, sys, pyautogui, pynput
from functools import partial
locate_events = {}
mouseController = pynput.mouse.Controller()
#packages: {package_name: []}
packages = {}
buttons = {}
tray_buttons = {}
load_functions = {}
unload_functions = {}
disabled_modules = {}

pressfunction = lambda _, x, y: (setattr(mouseController, "position", (x, y)), mouseController.press(pynput.mouse.Button.left), mouseController.release(pynput.mouse.Button.left))

class ImportTools():
    """
    Class:       ImportTools

    Description: Import and dynamicly reload all the modules
    """
    def __init__(self, path="packages/"):
        self.path = path
        self.modules = {}
        self.__ImportFromPath()
    def __ImportFromPath(self):
        for pl in os.listdir(self.path):
            new_path = f"{self.path}{pl}"
            if os.path.isfile(new_path):
                path = os.path.splitext(pl)[0]
                spec = importlib.util.spec_from_file_location(path, new_path)
                foo = importlib.util.module_from_spec(spec)
                buttons[path] = []
                disabled_modules[path] = False
                locate_events[path] = []
                self.modules[path] = foo
                spec.loader.exec_module(foo)
    def unload_module(self, parent_class, button_obj, name):
        disabled_modules[name] = True
        for button in buttons[name]:
            button.destroy()
        call_unload(parent_class, name)
        del self.modules[name]
        button_obj.configure(text=f"Load {name.capitalize()}", command=partial(parent_class.tools.load_module, parent_class, button_obj, name))
    def load_module(self, parent_class, button_obj, module):
        disabled_modules[module] = False
        button_obj.configure(text=f"Unload {module.capitalize()}", command = partial(parent_class.tools.unload_module, parent_class, button_obj, module))
        spec = importlib.util.spec_from_file_location(module, "{}{}.py".format(self.path, module))
        foo = importlib.util.module_from_spec(spec)
        buttons[module] = []
        self.modules[module] = foo
        spec.loader.exec_module(foo)
        call_init(parent_class, module)

def is_module_disabled(module):
    return disabled_modules.get(module)

def add_button(module_name, button):
    buttons[module_name].append(button)

def all_children(window):
    _list = window.winfo_children()
    for item in _list :
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list

def unforget(self, module_name):
    widget_list = all_children(self)
    for item in widget_list:
        item.pack()
    for button in buttons[module_name]:
        button.pack_forget()

def load_function(name):
    def func_wrap(func):
        load_functions[name] = func
    return func_wrap

def unload_function(name):
    def func_wrap(func):
        unload_functions[name] = func
    return func_wrap

def forget_all(func):
    def args_wrap(self):
        widget_list = all_children(self)
        for item in widget_list:
            item.pack_forget()
        func(self, lambda module_name: unforget(self, module_name))
    return args_wrap

def _call_init(self, module: str):
    v = load_functions[module]
    v(self)

def _call_unload(self, module: str):
    v = unload_functions[module]
    v(self)

def call_init(self, module=None):
    if module is None:
        for module in self.tools.modules.keys():
            _call_init(self, module)
    else:
        if (module in list(load_functions.keys())):
            _call_init(self, module)

def call_unload(self, module=None):
    if module is not None:
        if module in list(unload_functions):
            _call_unload(self, module)
    else:
        if (module in list(unload_function)):
            _call_unload(self, module)

# USAGE:
# click_on_locate("mymodule", [path1, path2], [conf1, conf2])
# click_on_locate("mymodule", path, conf)
# click_on_locate("mymodule", [{"confidence": 1, "path": "mypath"}, {"confidence": 1, "path": "mypath2"}])
def click_on_locate(module: str, pathes: list or str, confidences: list or float or int = 1):
    if type(pathes) == list:
        for j, i in enumerate(pathes):
            if (type(i) == dict):
                locate_event(module, i["path"], i.get("confidence") if i.get("confidence") is not None else 1)(pressfunction)
            elif (type(i) == list):
                locate_event(module, pathes[j], confidences[j])(pressfunction)
    else:
        locate_event(module, pathes, confidences)(pressfunction)
        

def locate_event(module, path, confidence=1):
    def wrap(func):
        locate_events[module].append([path, func, confidence])
    return wrap

def tray_button(name, **kwargs):
    def wrap(func):
        tray_buttons[name] = [func, kwargs]
    return wrap