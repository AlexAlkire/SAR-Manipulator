
"""
Front-end GUI for SAR Manipulator.
"""

__author__ = 'Alex Alkire'
__version__ = '0.1'
__license__ = 'MIT'

import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *


def foobar():
    print("fnc pressed")
    pass

class UI(Frame):
    def update_symbol_art(self, _image):
        _image = cv2.cvtColor(_image, cv2.COLOR_BGR2RGB)
        self.pil_image = _image
        self.tk_image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(_image))

    def __init__(self, master=None):
        self.pil_image = None
        self.tk_image = None
        super().__init__(master)
        master.geometry("512x512")
        master.resizable(False, False)
        master.title("SAR Manipulator")

        # Add Menus
        menu_bar = Menu(master)
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open .SAR", command=self.update)
        file_menu.add_command(label="Open .PNG", command=foobar)
        file_menu.add_command(label="Save .SAR", command=foobar)
        file_menu.add_command(label="SAVE .PNG", command=foobar)
        master.config(menu=menu_bar)

        # Set up Image to show in the window.
        image_canvas = Canvas(master, width=512, height=512)
        image_canvas.pack()
        self.image_label = Label(image_canvas)
        self.image_label.place(x=0, y=0)

    def update(self):
        self.image_label.configure(image=self.tk_image)


