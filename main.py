import tkinter as tk
from tkinter import filedialog as fd
def callback():
    name = fd.askopenfilename()


tk.Button(text='Click to Open File',
          command=callback).pack(fill=tk.X)

tk.mainloop()
