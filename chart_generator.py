"""Generator wykresów i diagramów
Autor: Piotr Frydman
"""
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
import matplotlib.pyplot as plt
import csv
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generator wykresów")
        self.geometry("300x100")
        #położenie elementów w oknie
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=3)

        self.fname = tk.Entry(self, bd=2)
        self.fname.grid(row=1, column=0)

        self.search = tk.Button(self, text="Szukaj", command=self.search_file)
        self.search.grid(row=1, column=2)

        self.l1 = tk.Label(self, text="Podaj nazwę pliku")
        self.l1.grid(row=0, column=0)

        self.lexp = tk.Label(self, text=".csv")
        self.lexp.grid(row=1, column=1)

        self.le = tk.Label(self, text="")
        self.le.grid(row=2, column=0)

    def search_file(self):
        self.file = self.fname.get()
        self.file += ".csv"

        # Wyszukuje plik w katalogach
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name == self.file:
                    os.chdir(root)
                    self.read_file(self.file)
                    self.le.config(text="")
                else:
                    self.le.config(text="Plik nie istnieje")

    def read_file(self, filename):
        with open(filename) as file:
            reader = csv.reader(file, delimiter=";")
            col_names = next(reader)

        # Przekazuje nazwy kolumn i pliku
        self.create_chart(col_names, filename)

    def create_chart(self, col_names, filename):
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

        # Komunikat błędów
        self.laberr = tk.Label(top, text="")
        self.laberr.grid(row=6, column=1)
        
        chtype = ["kolumnowy", "liniowy"]

        def configure_chart():
            # Przechowuje dane pobrane od użytkownika
            chart_config = {
                'data': '',
                'type': '',
                'labelx': '',
                'labely': '',
                'title': '',
                'datInd': 0,
                'typeInd': 0
            }

            # Wybór danych
            chart_config['data'] = data.get()

            # Wybór typu wykresu
            chart_config['type'] = chart_type.get()

            chart_config['labelx'] = osX.get()
            chart_config['labely'] = osY.get()
            chart_config['title'] = title.get()

            if chart_config['data'] not in col_names or chart_config['type'] not in chtype:
                    self.laberr.config(text="Proszę wybrać opcje z list")

            else:
                chart_config['datInd'] = col_names.index(data.get())
                chart_config['typeInd'] = chtype.index(chart_type.get())
                self.laberr.config(text="")
                self.draw_graph(chart_config, filename)

        ldata = tk.Label(top, text="Typ danych")
        ldata.grid(row=0, column=0)
        data = ttk.Combobox(top, values=col_names[1:], state="readonly")
        data.grid(row=0, column=1)
        data.set("Wybierz typ danych")

        lchart = tk.Label(top, text="Typ wykresu")
        lchart.grid(row=1, column=0)
        chart_type = ttk.Combobox(top, values=chtype, state="readonly")
        chart_type.grid(row=1, column=1)
        chart_type.set("Wybierz typ wykresu")

        # Tytuł wykresu
        ltitle = tk.Label(top, text="Tytuł wykresu").grid(row=3, column=0)
        title = tk.Entry(top, bd=3, width=25)
        title.grid(row=3, column=1)

        # Oznaczenie osi X
        loX = tk.Label(top, text="Nazwa osi X").grid(row=4, column=0)
        osX = tk.Entry(top, bd=3, width=25)
        osX.grid(row=4, column=1)

        # Oznaczenie osi Y
        loY = tk.Label(top, text="Nazwa osi Y").grid(row=5, column=0)
        osY = tk.Entry(top, bd=3, width=25)
        osY.grid(row=5, column=1)

        b = tk.Button(top, text="Utwórz", command=configure_chart)
        b.grid(row=7, column=3)

    def draw_graph(self, chartOpt, filename):
        read_data = []
        labels = []
        with open(filename) as f:
            reader = csv.reader(f, delimiter=";")
            data_row = next(reader)

            #pobranie danych
            for row in reader:
                csv_row = row[chartOpt['datInd']]
                read_data.append(float(csv_row))
                names = row[0]
                labels.append(names)
            f.close()

            # Tworzenie wykresu
            if chartOpt['typeInd'] == 0:
                fig, ax = plt.subplots(figsize=(6, 6))
                ax.bar(labels, read_data)

            if chartOpt['typeInd'] == 1:
                plt.plot(labels, read_data)

            plt.title(chartOpt['title'])
            plt.xlabel(chartOpt['labelx'])
            plt.ylabel(chartOpt['labely'])
            plt.show()          

app = App()
app.mainloop()
