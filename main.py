import threading
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd

import magic

from Huffman import Huffman

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


def huff_load():
    global huff_data
    global data
    global huffer
    huff_data = huffer.archive(data)
    return


def rle_load():
    global rle
    global rle_data
    global data
    rle_data = rle.archive(data)
    return


def unarchiver():
    global data
    global file_name
    global name
    global finished
    signature = data[:7]
    unarchived = b''
    if signature == b'ACEARCH':
        unarchived = huffer.unarchive(name)
    elif signature == b'ACEARCR':
        unarchived = rle.unarchive(name)
    else:
        print("What da heeeel")
    extension = check_file_extension(unarchived)
    with open(f"{file_name}{extension}", "wb") as f:
        f.write(unarchived)
    finished = True
    return

def file_selector():
    global name
    name = fd.askopenfilename()
    start_button.pack_forget()
    start_button.pack()
def callback():
    global rle
    global data
    global finished
    global huffer
    global finished
    global file_name
    global name
    finished = False
    text.pack()
    threading.Thread(target=load_bar).start()
    with open(name, 'rb') as data:
        data = data.read()
        huffer = Huffman()
        rle = RLE()
        if name[-6::] == "ultarc":
            if f_name.get() != 'Optionally enter the output file name here':
                file_name = f_name.get()
            else:
                if '.' in name:
                    file_name = f"{name.split('.')[0]}_unarchivated"
                else:
                    file_name = f"{name}_unarchivated"
            t2 = threading.Thread(target=unarchiver)
            if not t2.is_alive():
                t2.start()
        else:
            if f_name.get() != 'Optionally enter the output file name here':
                file_name = f_name.get()
            else:
                if '.' in name:
                    file_name = f"{name.split('.')[0]}_archivated"
                else:
                    file_name = f"{name}_archivated"
            huffman_thread = threading.Thread(target=huff_load)
            rle_thread = threading.Thread(target=rle_load)
            if not huffman_thread.is_alive():
                huffman_thread.start()
            if not rle_thread.is_alive():
                rle_thread.start()
            huffman_thread.join()
            rle_thread.join()

            with open(f"{file_name}.ultarc", "wb") as f:
                f.write(b'ACEARC')
                if len(huff_data) < len(rle_data):
                    f.write(b'H')
                    f.write(huff_data)
                else:
                    f.write(b'R')
                    f.write(rle_data)
            finished = True


def on_entry_click(event):
    if textBox.get() == 'output':
        textBox.delete(0, 'end')
        textBox.config(font=('Arial', 16))


text_label = tk.Label(root, text='Welcome to the "Ultarc" archivator! Click the button below to select a file.', font=('Arial', 24),
                      padx=10, pady=20, anchor='center')
text_label.pack()
frame = Frame()
textBox = Entry(frame, width=14, font=('Arial', 16, 'italic'), justify=CENTER, textvariable=f_name)
textBox.insert(0, "Optionally enter the output file name here")
textBox.bind('<FocusIn>', on_entry_click)
textBox.pack(side=LEFT, padx=20, expand=True, fill=BOTH)
b = tk.Button(frame, text='Click to Open File',
          command=file_selector, height=1)
b.pack(side=RIGHT, padx=20, expand=True, fill=BOTH)

frame.pack(expand=True, fill=X, pady=10)
start_button = tk.Button(root, text='Start magic!',
          command=callback, height=1, fg="purple")

text = Label(root, text="Loading", font=('Arial', 20, 'bold'), fg="yellow", pady=20)
list = ["       ", ".      ", "..     ", "...    ", "....   ", ".....  ", "...... ", "......."]


def load_bar():
    k = 0
    while not finished:
        k += 1
        text.config(text="Magic in proccess" + list[k % 8], fg="yellow")
        text.update()
        time.sleep(0.1)
    text.config(text="Magic has happened!", fg="green")
    b.focus()
    return


tk.mainloop()
