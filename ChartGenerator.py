"""
Project: Chart and diagram generator
Author: Piotr Frydman
"""
import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import os

class ChartGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chart generator")
        self.geometry("250x100+300+250")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Set filename").place(x=25,y=25)
        self.filename=tk.Entry(self, bd=2)
        self.filename.place(x=25,y=55)
        tk.Button(self, text="Search",
                  command=self.search_file).place(x=190,y=50)
        tk.Label(self, text=".csv").place(x=152,y=55)
    
    def search_file(self):
        self.file = self.filename.get() + ".csv"
        file_found = False
        
        #wyszukuje plik w katalogach
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name == self.file:
                    os.chdir(root)
                    self.read_file(self.file)
                    file_found = True
                else:
                    self.filename.delete(0,'end')
                  
        if not file_found:
            messagebox.showerror("Error", "File not found")
                
    def read_file(self, filename):
        #read headers to options
        with open(filename) as file:
            reader = csv.reader(file, delimiter=";")
            headers = next(reader)
        file.close()
        self.configure_chart(headers, filename)

    def configure_chart(self, headers, filename):
        top = Toplevel()
        top.geometry("280x250+560+200")
        top.title("Configuring chart")
        top.grab_set()
        top.focus()    
        
        def create_chart():
            #przechowuje dane pobrane od użytkownika
            options = {
                'data': data.get(),
                'type': chart_type.get(),
                'labelx': osX.get(),
                'labely': osY.get(),
                'title': title.get(),
                'datInd': 0,
                'typeInd': 0
            }
            
            if options['data'] not in headers or options['type'] not in chtype:
                    messagebox.showinfo("Info", "Select options from lists")

            else:
                options['datInd'] = headers.index(data.get())
                options['typeInd'] = chtype.index(chart_type.get())
                self.draw_graph(options, filename)

        tk.Label(top, text="Data type").place(x=20,y=10)
        data = ttk.Combobox(top, values=headers[1:], state="readonly")
        data.place(x=100, y=10)
        data.set("Select data type")

        chtype = ["column", "line"]
        tk.Label(top, text="Chart type").place(x=20,y=40)
        chart_type = ttk.Combobox(top, values=chtype, state="readonly")
        chart_type.place(x=100,y=40)
        chart_type.set("Select chart type")

        tk.Label(top, text="Chart title").place(x=20,y=80)
        title=tk.Entry(top, bd=3, width=25)
        title.place(x=100,y=80)

        tk.Label(top, text="X axis label").place(x=20,y=120)
        osX=tk.Entry(top, bd=3, width=25)
        osX.place(x=100,y=120)

        tk.Label(top, text="Y axis label").place(x=20,y=160)
        osY=tk.Entry(top, bd=3, width=25)
        osY.place(x=100,y=160)

        tk.Button(top, text="Create",width=20,bd=4,bg="#FFE5CC",
                  command=create_chart).place(x=60,y=200)

    def draw_graph(self, options, filename):
        read_data, labels = [],[]
        with open(filename) as file:
            reader = csv.reader(file, delimiter=";")
            data_row = next(reader)
                
            #read data from file
            for row in reader:
                csv_row = row[options['datInd']]
                read_data.append(float(csv_row))
                names = row[0]
                labels.append(names)

            if options['typeInd'] == 0:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.bar(labels, read_data)

            if options['typeInd'] == 1:
                plt.plot(labels, read_data)
            file.close()
            
            plt.title(options['title'])
            plt.xlabel(options['labelx'])
            plt.ylabel(options['labely'])
            plt.show()          
        
app = ChartGenerator()
app.mainloop()
