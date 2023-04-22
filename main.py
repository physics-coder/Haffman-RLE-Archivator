import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd
from Huffman import Huffman
import time
import magic
import threading
from PIL import Image, ImageTk
root = tk.Tk()
root.title("Ultarc file archivator")
f_name = tk.StringVar(root)

def check_file_extension(file_bytes):
    file_type = magic.from_buffer(file_bytes)
    if 'PDF' in file_type:
        return '.pdf'
    elif 'JPEG' in file_type:
        return '.jpg'
    elif 'PNG' in file_type:
        return '.png'
    elif 'text' in file_type:
        return '.txt'
    elif 'Audio file' in file_type:
        return '.mp3'
    else:
        return None

from RLE import RLE
def work():
    global finished
    finished = False
    if f_name.get() != '':
        file_name = f_name.get()
    else:
        file_name = "output"
    name = fd.askopenfilename()
    text.pack()
    with open(name, 'rb') as data:
        data = data.read()
        huffer = Huffman()
        rle = RLE()
        if name[-6::] == "ultarc":
            signature = data[:7]
            unarchived = b''
            if signature == b'ACEARCH':
                unarchived = huffer.unarchive(name)
            elif signature == b'ACEARCR':
                unarchived = rle.unarchive(name)
            else:
                print("What da heeeel")
            extension = check_file_extension(unarchived)
            with open (f"{file_name}{extension}", "wb") as f:
                f.write(unarchived)
            finished = True
        else:
            huff_data = huffer.archive(data)
            rle_data = rle.archive(data)
            with open(f"{file_name}.ultarc", "wb") as f:
                f.write(b'ACEARC')
                if len(huff_data) < len(rle_data):
                    f.write(b'H')
                    f.write(huff_data)
                else:
                    f.write(b'R')
                    f.write(rle_data)
            finished = True
def callback():
    global finished
    finished = False
    t2 = threading.Thread(target=work)
    t1.start()
    t2.start()


def on_entry_click(event):
    if textBox.get() == 'output':
        textBox.delete(0, 'end')
        textBox.config(font=('Arial', 16))

text_label = tk.Label(root, text='Welcome to the "Ultarc" archivator! You can click the button below to select a file.'
                                 '\n If you upload a .ultarc file, it will be unarchivated, any'
                                 ' other file will be archivated. \n If you want to specify a particular output file name,'
                                 ' enter it in the text field below \n without the file extension.', font=('Arial', 24), padx=10, pady=30, anchor='center')
text_label.pack()
frame = Frame()
textBox = Entry(frame, width=10, font=('Arial', 16, 'italic'), justify=CENTER, textvariable=f_name)
textBox.insert(0, "output")
textBox.bind('<FocusIn>', on_entry_click)
textBox.pack(side=LEFT, padx=20, expand=True, fill=BOTH)
tk.Button(frame, text='Click to Open File',
          command=callback, height=1).pack(side=RIGHT, padx=20, expand=True, fill=BOTH)

frame.pack(expand=True, fill=X, pady=40)

text = Label(root, text="Loading", font=('Arial', 20, 'bold'), fg="yellow")
list = ["       ", ".      ", "..     ", "...    ", "....   ", ".....  ", "...... ", "......."]

def load_bar():
    global finished
    k = 0
    while not finished:
        k+=1
        text.config(text="Loading" + list[k % 8])
        text.update()
        time.sleep(0.1)
    text.config(text="Finished", fg="green")
t1 = threading.Thread(target=load_bar)


tk.mainloop()