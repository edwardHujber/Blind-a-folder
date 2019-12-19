from tkinter import filedialog, messagebox
import tkinter as tk
import os
import random
import string
import pickle
import csv
import math


def rando_string(k):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid()
        self.configure(background='LightBlue2')
        self.winfo_toplevel().title("Blind-a-folder")
        self.create_buttons()

    def create_buttons(self):
        self.button_frame = tk.Frame(self)
        self.button_frame.configure(background='LightBlue2')
        self.button_frame.grid(row=0, padx=20, pady=10)
        self.blind_button = tk.Button(self.button_frame, text="BLIND", command=self.blind, font=("Helvetica", 30))
        self.blind_button.grid(row=0, column=0, pady=5)
        self.unblind_button = tk.Button(self.button_frame, text="UNBLIND", command=self.unblind, font=("Helvetica", 30))
        self.unblind_button.grid(row=1, column=0, pady=5)

    def blind(self):
        directory = filedialog.askdirectory() + '/'
        if directory == '/':
            return
        items_in_dir = os.listdir(directory)
        N_items_in_dir = len(items_in_dir)
        proceed_msg = "Selected directory: " + directory + "\n\nWill be blinding items like:\n" + '\n'.join(items_in_dir[:10])
        if N_items_in_dir > 10:
            proceed_msg = proceed_msg + '\n\n... and ' + str(N_items_in_dir - 10) + ' more.'
        if not messagebox.askokcancel("Proceed???", proceed_msg):
            return
        cypher = {}
        for i in items_in_dir:
            rando_file_base = rando_string(6 + math.ceil(math.log10(N_items_in_dir)))
            cypher[i] = rando_file_base
        ok = 0
        for key in cypher:
            os.rename(directory + key, directory + cypher[key])
            ok = ok + 1
        save_to = directory + 'blinding_' + rando_string(4) + '.key'
        with open(save_to, 'wb') as f:
            pickle.dump(cypher, f, pickle.HIGHEST_PROTOCOL)
        messagebox.showinfo("Items blinded!!", "Renamed " + str(ok) + ' of ' + str(N_items_in_dir) + " items.\nKey saved to: " + save_to)

    def unblind(self):
        pkl_file_location = filedialog.askopenfilename(title="Please select a key:", filetypes=[('key file', '.key')])
        if pkl_file_location == '':
            return
        cyph_name = os.path.splitext(os.path.basename(pkl_file_location))[0]
        dir_name = os.path.dirname(pkl_file_location) + '/'
        nFiles = len(os.listdir(dir_name))
        with open(pkl_file_location, 'rb') as f:
            cypher = pickle.load(f)
        ok = 0
        for key in cypher:
            try:
                os.rename(dir_name + cypher[key], dir_name + key)
                ok = ok + 1
            except FileNotFoundError:
                pass
        messagebox.showinfo("Items unblinded!!", "Folder has " + str(nFiles - 1) + " other items.\nKey had " + str(len(cypher)) + " entries.\nItems renamed successfully: " + str(ok))
        with open(dir_name + cyph_name + '.csv', 'w', newline='') as f:
            listWriter = csv.writer(f)
            for k in cypher:
                listWriter.writerow([k, cypher[k]])


root = tk.Tk()
app = Application(master=root)
app.mainloop()
