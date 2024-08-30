## ChartGenerator
A program that generates a chart based on data from a spreadsheet

## Table of contents
* Description
* Technologies
* Setup

## Description
The program takes the file name of spreadsheet entered by the user and searches for 
it in directories. Then it allows you to select a column with data and create 
a chart based on it.

The application was written in Python. Has a graphical user interface (GUI)
created using the Python standard library - Tkinter. They were used in the project
also other Python built-in libraries, including: os (do
searching for a file in the system) and csv (reading files). 

![Search file window](https://github.com/FrydmanPiotr/ChartGenerator/blob/main/images/searchwin.png)
![Configure chart window](https://github.com/FrydmanPiotr/ChartGenerator/blob/main/images/configurechart.png)

## Technologies 
Project is created with:
* Python 3.11

## Setup
To run this project, install locally following Python modules:
* matplotlib
  
Install Matplotlib libary by using this commands in system console
using PIP (Python package manager):

```
python -m pip install -U pip
python -m pip install -U matplotlib
```
