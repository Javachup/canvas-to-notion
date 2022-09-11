from tkinter import *
from tkinter import filedialog as fd
import tkinterHelper.Console as Console
from threading import Thread

import main

def selectFile():
    filetypes = (('Info File', '*.json'), ('All files', '*.*'))

    f = fd.askopenfilename(title='Open Info.json', initialdir='.', filetypes=filetypes)

    btn.config(state='disable')

    main.Run(f)

window = Tk()
window.title("Testing! :)")
window.configure(width=1000, height=700)

btn = Button(window, text="Browse", command=Thread(target=selectFile).start)
btn.pack(pady=20)

cmd = Console.Console(window)
cmd.pack(pady=20)

print("Click browse and find your info.json")
window.mainloop()
