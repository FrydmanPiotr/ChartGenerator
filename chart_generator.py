"""Generator wykresów i diagramów
Autor: Piotr Frydman
"""
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import os

data_type = []

def read_file():
    try:
        file = e1.get()
        if file != "": 
            with open(file) as f:
                reader = csv.reader(f, delimiter=";")
                data_type = next(reader)
            f.close()
            le.config(text="")

            #przekazuje nazwy kolumn i pliku
            create_chart(data_type, file)
            
        else:
            le.config(text="Proszę podać nazwę pliku")
            
    except FileNotFoundError:
        le.config(text="Plik o tej nazwie nie istnieje")
    
def create_chart(dtype, filename):
    top = Toplevel()
    top.geometry("400x200")
    top.title("Tworzenie wykresu")
    top.grab_set()
    top.focus()

    chtype = ["kolumnowy", "liniowy"]
    
    def configure_chart():
        #wybór danych
        select_data = data.get()
            
        #wybór typu wykresu
        chart_type = chart.get()

        x = osX.get()
        y = osY.get()
        chtitle = title.get()
        
        if select_data not in dtype or chart_type not in chtype:
            laberr.config(text="Proszę wybrać opcje z list")
        else:
            datind = dtype.index(select_data)
            graph = chtype.index(chart_type)
            laberr.config(text="")
            draw_graph(datind, graph,chtitle, x,y)
                                                 
    data = ttk.Combobox(top, values=dtype, state="readonly")
    data.grid(row = 0, column = 0)
    data.set("Wybierz typ danych")
        
    chart = ttk.Combobox(top, values=chtype, state="readonly")
    chart.grid(row = 1, column = 0)
    chart.set("Wybierz typ wykresu")

    #tytuł wykresu
    ltitle=Label(top, text="Tytuł wykresu")
    ltitle.grid(row=3,column=0)
    title= Entry(top,bd=3, width=25)
    title.grid(row=3,column=1)

    #oznaczenie osi X
    loX=Label(top, text="Nazwa osi X")
    loX.grid(row=4,column=0)
    osX= Entry(top,bd=3, width=25)
    osX.grid(row=4,column=1)
    
    #oznaczenie osi Y
    loY=Label(top, text="Nazwa osi Y")
    loY.grid(row=5,column=0)
    osY= Entry(top,bd=3,width=25)
    osY.grid(row=5,column=1)
    
    b = Button(top, text="Utwórz", command=configure_chart)
    b.grid(row=0,column=1)

    laberr = Label(top, text = "")
    laberr.grid(row=6,column=0)
    
    def draw_graph(dati,chai,title, osx,osy):
        read_data = []
        rd = []
        with open(filename) as f:
            reader = csv.reader(f, delimiter=";")
            data_row = next(reader)
                    
            for row in reader:
                csv_row = float(row[dati])
                rd.append(csv_row)
                read_data = tuple(rd)
        f.close()
        
        numbers = []
        i = 0
        temp = []
        #dodanie etykiet
        for i in range(len(rd)):
            numbers.append(i+1)
            temp.append(str(numbers[i]))
            labels = (tuple(temp))

        #tworzenie wykresu
        if chai == 0:
            plt.bar(labels, read_data)
        if chai == 1:
            plt.plot(labels, read_data)

        plt.title(title) 
        plt.xlabel(osx)
        plt.ylabel(osy)              
        plt.show()
            
root = Tk()
root.title("Generator wykresów")
root.geometry('360x100')

l1 = Label(root, text = "Podaj nazwę pliku", pady=8)
l1.grid(row=0,column=0)

e1= Entry(root, bd=3, width=25)
e1.grid(row=1,column=0)

b = Button(root, text="OK", command=read_file)
b.grid(row=1,column=1)

le = Label(root, text = "", pady=6)
le.grid(row=2,column=0)

root.mainloop()

