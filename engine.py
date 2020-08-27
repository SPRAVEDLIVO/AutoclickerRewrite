import os, importlib, sys
locate_events = {}
#packages: {package_name: []}
packages = {}
buttons = {}
tray_buttons = {}

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
                self.modules[path] = foo
                spec.loader.exec_module(foo)
    def unload_module(self, parent_class, button_obj, name):
        for button in buttons[name]:
            button.destroy()
        del buttons[name]
        del self.modules[name]
        button_obj.configure(text=f"Load {name.capitalize()}")
    def load_module(self, parent_class, module):
        spec = importlib.util.spec_from_file_location(module, "{}{}.py".format(self.path, module))
        foo = importlib.util.module_from_spec(spec)
        buttons[module] = []
        self.modules[module] = foo
        spec.loader.exec_module(foo)
        call_init(parent_class, module)

    

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


def forget_all(func):
    def args_wrap(self):
        widget_list = all_children(self)
        for item in widget_list:
            item.pack_forget()
        func(self, lambda module_name: unforget(self, module_name))
    return args_wrap

def _call_init(self, module: object):
    if hasattr(module, "init_module"):
            module.init_module(self)

def call_init(self, module=None):
    if module is None:
        for module in self.tools.modules.values():
            _call_init(self, module)
    else:
        _call_init(self, self.tools.modules[module])


def locate_event(path):
    def wrap(func):
        locate_events[path] = func
    return wrap

def tray_button(name, **kwargs):
    def wrap(func):
        tray_buttons[name] = [func, kwargs]
    return wrap