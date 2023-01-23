from tkinter import *
from tkinter import filedialog as fd
import tkinterHelper.Console as Console
from MyThreads import CallBackThread
import os

import CanvasToNotion as c2n

class App:
    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Canvas To Notion")

        self.btn_fileSelect = Button(self.window, text="Browse", command=self.selectFile)
        self.btn_fileSelect.place(x=10, y=20)

        self.ent_fileNameEntry = Entry(self.window)
        self.ent_fileNameEntry.place(x=70, y=25, width=260)
        self.ent_fileNameEntry.insert(0, os.getcwd() + "\info.json")

        self.btn_run = Button(self.window, text="Run Program", command=self.run_thread)
        self.btn_run.place(x=500, y=20)

        self.cmd_console = Console.Console(self.window)
        self.cmd_console.pack(pady=50)

        print("Click browse and find your info.json")
        self.window.mainloop()

    def selectFile(self):
        filetypes = (('Info File', '*.json'), ('All files', '*.*'))

        f = fd.askopenfilename(title='Open Info.json', initialdir='.', filetypes=filetypes)
        if f == '':
            return

        self.ent_fileNameEntry.delete(0, END)
        self.ent_fileNameEntry.insert(0, f)

    def run_thread(self):
        filename = self.ent_fileNameEntry.get()
        file = {}

        extention = os.path.splitext(filename)[1]

        if not extention:
            print('Path not valid!')
            return

        if extention != '.json':
            print('File must be a .json file!')
            return

        try:
            file = open(filename, mode='r')
        except (FileNotFoundError):
            print('File Not Found!')
            return

        self.btn_run["state"] = "disabled"

        self.thread = CallBackThread(target=c2n.Run, args=[file], callback=self.thread_done)
        self.thread.start()

    def thread_done(self):
        self.btn_run["state"] = "normal"