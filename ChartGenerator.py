"""
Generator wykresów i diagramów
Autor: Piotr Frydman
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
        self.title("Generator wykresów")
        self.geometry("300x100+500+250")
        self.resizable(False, False)
        
        #położenie elementów w oknie
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=3)
        self.create_widgets()

    def create_widgets(self):
        self.name = tk.Label(self, text="Podaj nazwę pliku")
        self.name.grid(row=0, column=0)
        self.filename = tk.Entry(self, bd=2)
        self.filename.grid(row=1, column=0)
        self.search = tk.Button(self, text="Szukaj", command=self.search_file)
        self.search.grid(row=1, column=2)
        self.extension = tk.Label(self, text=".csv")
        self.extension.grid(row=1, column=1)
    
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
            messagebox.showerror("Błąd", "Plik nie istnieje")
                
    def read_file(self, filename):
        with open(filename) as file:
            reader = csv.reader(file, delimiter=";")
            columns_names = next(reader)
        file.close()

        #przekazuje nazwy kolumn i pliku
        self.create_chart(columns_names, filename)

    def create_chart(self, columns_names, filename):
        top = Toplevel()
        top.geometry("400x200")
        top.title("Tworzenie wykresu")
        top.grab_set()
        top.focus()
        
        top.columnconfigure(0, weight=3)
        top.columnconfigure(1, weight=3)
        top.columnconfigure(2, weight=2)

        top.rowconfigure(0, weight=2)
        top.rowconfigure(1, weight=2)          
       
        chtype = ["kolumnowy", "liniowy"]

        def configure_chart():
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
            
            if options['data'] not in columns_names or options['type'] not in chtype:
                    messagebox.showerror("Błąd", "Wybierz opcje z list")

            else:
                options['datInd'] = columns_names.index(data.get())
                options['typeInd'] = chtype.index(chart_type.get())
                self.draw_graph(options, filename)

        ldata = tk.Label(top, text="Typ danych").grid(row=0, column=0)
        data = ttk.Combobox(top, values=columns_names[1:], state="readonly")
        data.grid(row=0, column=1)
        data.set("Wybierz typ danych")

        lchart = tk.Label(top, text="Typ wykresu").grid(row=1, column=0)
        chart_type = ttk.Combobox(top, values=chtype, state="readonly")
        chart_type.grid(row=1, column=1)
        chart_type.set("Wybierz typ wykresu")

        #tytuł wykresu
        ltitle = tk.Label(top, text="Tytuł wykresu").grid(row=3, column=0)
        title = tk.Entry(top, bd=3, width=25)
        title.grid(row=3, column=1)

        #oznaczenie osi X
        loX = tk.Label(top, text="Nazwa osi X").grid(row=4, column=0)
        osX = tk.Entry(top, bd=3, width=25)
        osX.grid(row=4, column=1)

        #oznaczenie osi Y
        loY = tk.Label(top, text="Nazwa osi Y").grid(row=5, column=0)
        osY = tk.Entry(top, bd=3, width=25)
        osY.grid(row=5, column=1)

        b = tk.Button(top, text="Utwórz", command=configure_chart)
        b.grid(row=7, column=3)

    def draw_graph(self, options, filename):
        read_data = []
        labels = []
        with open(filename) as file:
            reader = csv.reader(file, delimiter=";")
            data_row = next(reader)
                
            #pobranie danych
            for row in reader:
                csv_row = row[options['datInd']]
                read_data.append(float(csv_row))
                names = row[0]
                labels.append(names)

            #tworzenie wykresu
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
