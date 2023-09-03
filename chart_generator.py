"""Gnerator wykresów i diagramów
Autor: Piotr Frydman
"""
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import os

data_type = []

def read_file():
    file = str(e1.get())
  
    with open(file) as f:
        reader = csv.reader(f, delimiter=";")
        data_type = next(reader)
    f.close()

    create_chart(data_type, file)
    
def create_chart(dtype, filename):
    top = Toplevel()
    top.geometry("200x70")
    top.title("Tworzenie wykresu")

    def select():
        #wybór danych
        select_data = data.get()
        i = dtype.index(select_data)
        draw_graph(i)

    def draw_graph(j):
        read_data = []
        rd = []
        with open(filename) as f:
            reader = csv.reader(f, delimiter=";")
            data_row = next(reader)
                    
            for row in reader:
                ree = float(row[j])
                rd.append(ree)
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
                
        plt.bar(labels, read_data)
        plt.xlabel("Oś X")
        plt.ylabel("Oś Y")
        plt.title("Tytuł wykresu")              
        plt.show()
        
    data = ttk.Combobox(top, values=dtype, state="readonly")
    data.grid(row = 0, column = 0)
    data.set("Wybierz typ danych")
    
    b = Button(top, text="Utwórz", command=select)
    b.grid(row=0,column=1)
    
root = Tk()
root.title("Generator wykresów")
root.geometry('360x100')

l1 = Label(root, text = "Podaj nazwę pliku")
l1.grid(row=0,column=0)
e1= Entry(root, bd =3, width=25)
e1.grid(row=1,column=0)
b = Button(root, text="OK", command=read_file)
b.grid(row=1,column=1)

root.mainloop()

