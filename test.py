import Tkinter as tk
import time
def file1():
    with open('3.txt') as f:
        for i in f:
            a.insert(tk.END, i)
            a.insert(tk.END, '-'*20 + '\n')
            time.sleep(0.1)
            a.update()
            a.see(tk.END)

root = tk.Tk()
a = tk.Text(root)
b = tk.Scrollbar(root)
a['yscrollcommand'] = b.set
b['command'] = a.yview
b.grid(row = 1, column = 1, rowspan = 4)
a.grid(row=0, column=0, columnspan=4)
tk.Button(root, text='Go', command=file1).grid(row=1, column=2)



root.mainloop()