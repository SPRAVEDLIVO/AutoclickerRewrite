# Managing modules script.
import engine, os
from functools import partial

@engine.forget_all
def place_buttons(self, unforget_callback):
    for module in os.listdir("packages/"):
        module_path = os.path.join("packages", module)
        if (os.path.isfile(module_path)):
            module = os.path.splitext(module)[0]
            # Module is loaded
            if (module in self.tools.modules):
                module_button = self.add_button("modules", text = f"Unload {module.capitalize()}")
                module_button.configure(command = partial(self.tools.unload_module, self, module_button, module))
            else:
                module_button = self.add_button("modules", text = f"Load {module.capitalize()}")
                module_button.configure(command = partial(self.tools.load_module, self, module_button, module))
            module_button.pack()
    self.add_button("modules", text = "Exit", command = partial(unforget_callback, "modules")).pack()

        

@engine.load_function("modules")
def init_module(self):
    modules_button = self.add_button("modules", can_forget=False, text="Modules", command = partial(place_buttons, self), width=10)
    modules_button.pack()