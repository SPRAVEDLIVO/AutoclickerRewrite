import tkinter as tk

class Button(tk.Button):
    def __init__(self, can_forget=True, **kwargs):
        self.can_forget = can_forget
        super().__init__(**kwargs)
    def pack_forget(self):
        if (self.can_forget):
            super().pack_forget()