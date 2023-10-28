"""Generator wykresów i diagramów
Autor: Piotr Frydman
"""
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import os

def search_file():
    file = fname.get()
    #wyszukuje plik w katalogach
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name == file:
                os.chdir(root)
                read_file(file)
                le.config(text="")
            else:
                le.config(text="Plik nie istnieje")
            
def read_file(file):
    with open(file) as f:
        reader = csv.reader(f, delimiter=";")
        col_names = next(reader)
    f.close()
    
    #przekazuje nazwy kolumn i pliku
    create_chart(col_names, file)    
    
def create_chart(dtype, filename):
    top = Toplevel()
    top.geometry("400x200")
    top.title("Tworzenie wykresu")
    top.grab_set()
    top.focus()

    top.columnconfigure(0,weight=3)
    top.columnconfigure(1,weight=3)
    top.columnconfigure(2,weight=2)

    top.rowconfigure(0,weight=2)
    top.rowconfigure(1,weight=2)
    
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

    ldata=Label(top, text="Typ danych")
    ldata.grid(row=0,column=0)
    data = ttk.Combobox(top, values=dtype, state="readonly")
    data.grid(row = 0, column = 1)
    data.set("Wybierz typ danych")

    lchart=Label(top, text="Typ wykresu")
    lchart.grid(row=1,column=0)    
    chart_type = ttk.Combobox(top, values=chtype, state="readonly")
    chart_type.grid(row = 1, column = 1)
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

    #komunikat błędów
    laberr = Label(top, text = "")
    laberr.grid(row=6,column=1)
    
    b = Button(top, text="Utwórz", command=configure_chart)
    b.grid(row=7,column=3)
    
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
            fig,ax=plt.subplots(figsize=(6,6))
            ax.bar(labels, read_data)
            
        if chartOpt['typeInd'] == 1:
            plt.plot(labels, read_data)

                
        plt.title(chartOpt['title']) 
        plt.xlabel(chartOpt['labelx'])
        plt.ylabel(chartOpt['labely'])              
        plt.show()
            
root = Tk()
root.title("Generator wykresów")
root.geometry('300x100')

#położenie elementów w oknie
root.columnconfigure(0,weight=8)
root.columnconfigure(1,weight=1)
root.columnconfigure(2,weight=3)

root.rowconfigure(0,weight=2)
root.rowconfigure(1,weight=2)

l1 = Label(root, text = "Podaj nazwę pliku")
l1.grid(row=0,column=0)

fname = Entry(root, bd=3)
fname.grid(row=1,column=0)

confirm = Button(root, text="Otwórz", command=search_file)
confirm.grid(row=1,column=2)

le = Label(root, text = "")
le.grid(row=2,column=0)

root.mainloop()

