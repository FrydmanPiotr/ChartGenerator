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
        le.config(text="Plik nie istnieje")
    
def create_chart(dtype, filename):
    top = Toplevel()
    top.geometry("400x200")
    top.title("Tworzenie wykresu")
    top.grab_set()
    top.focus()

    chtype = ["kolumnowy", "liniowy"]
    
    def configure_chart():
        #przechowuje dane pobrane od użytkownika
        chart_config = {
            'data':'',
            'type':'',
            'labelx':'',
            'labely':'',
            'title':'',
            'datInd':0,
            'typeInd':0
            }

        #wybór danych
        chart_config['data'] = data.get()
            
        #wybór typu wykresu
        chart_config['type'] = chart_type.get()

        chart_config['labelx'] = osX.get()
        chart_config['labely'] = osY.get()
        chart_config['title'] = title.get()
                
        if chart_config['data'] not in dtype or chart_config['type'] not in chtype:
            laberr.config(text="Proszę wybrać opcje z list")
        
        else:
            chart_config['datInd'] = dtype.index(data.get())
            chart_config['typeInd'] = chtype.index(chart_type.get())
            laberr.config(text="")
            draw_graph(chart_config)
                                                 
    data = ttk.Combobox(top, values=dtype, state="readonly")
    data.grid(row = 0, column = 0)
    data.set("Wybierz typ danych")
        
    chart_type = ttk.Combobox(top, values=chtype, state="readonly")
    chart_type.grid(row = 1, column = 0)
    chart_type.set("Wybierz typ wykresu")

    #tytuł wykresu
    ltitle=Label(top, text="Tytuł wykresu").grid(row=3,column=0)
    title= Entry(top,bd=3, width=25)
    title.grid(row=3,column=1)

    #oznaczenie osi X
    loX=Label(top, text="Nazwa osi X").grid(row=4,column=0)
    osX= Entry(top,bd=3, width=25)
    osX.grid(row=4,column=1)
    
    #oznaczenie osi Y
    loY=Label(top, text="Nazwa osi Y").grid(row=5,column=0)
    osY= Entry(top,bd=3,width=25)
    osY.grid(row=5,column=1)
    
    b = Button(top, text="Utwórz", command=configure_chart)
    b.grid(row=0,column=1)

    laberr = Label(top, text = "")
    laberr.grid(row=6,column=0)
    
    def draw_graph(chartOpt):
        read_data = []
        with open(filename) as f:
            reader = csv.reader(f, delimiter=";")
            data_row = next(reader)
                    
            for row in reader:
                csv_row = float(row[chartOpt['datInd']])
                read_data.append(csv_row)
                
        f.close()
        
        numbers = []
        temp = []
        #tworzenie domyślnych etykiet danych na osi X
        for i in range(len(read_data)):
            numbers.append(i+1)
            temp.append(str(numbers[i]))
            labels = (tuple(temp))

        #tworzenie wykresu
        if chartOpt['typeInd'] == 0:
            plt.bar(labels, read_data)
        if chartOpt['typeInd'] == 1:
            plt.plot(labels, read_data)

        plt.title(chartOpt['title']) 
        plt.xlabel(chartOpt['labelx'])
        plt.ylabel(chartOpt['labely'])              
        plt.show()
            
root = Tk()
root.title("Generator wykresów")
root.geometry('240x100')

l1 = Label(root, text = "Podaj nazwę pliku").grid(row=0,column=0)

e1= Entry(root, bd=3)
e1.grid(row=1,column=0)
confirm = Button(root, text="OK", command=read_file).grid(row=1,column=1)
le = Label(root, text = "")
le.grid(row=2,column=0)

root.mainloop()

