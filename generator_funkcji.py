# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk as ttk
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
from math import *

style.use('ggplot')


class Plot(Frame):
    u"""Klasa odpowiada za stworzenie aplikacji jednookienkowej. Służy do wygenerowania wykresów
    poprzez podanie wzoru i zakresu."""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()

    def createWidgets(self):
        u"""Funkcja tworzy cały widok aplikacji. Generuje pola do wprowadzenia danych, przyciski
        oraz płótno do rysowania wykresów."""
        self.master.title("Kreator wykresów funkcji")
        self.master.geometry('1100x600+200+50')

        self.grid()

        self.write_formula = ttk.Label(self, text="Wpisz wzór funkcji: ", borderwidth=10)
        self.write_formula.grid(row=1, column=0, pady=15)
        self.function_formula = Entry(self)
        self.function_formula.grid(row=1, column=1, pady=15)

        self.frame = Frame(self)
        self.frame.grid(row=2, column=0, rowspan=5, columnspan=3)

        self.sin = Button(self.frame, text="sin", width=5, command=lambda: self.build_formula('sin(x)'))
        self.sin.grid(row=1, column=0)
        self.cos = Button(self.frame, text="cos", width=5, command=lambda: self.build_formula('cos(x)'))
        self.cos.grid(row=1, column=1)
        self.tan = Button(self.frame, text="tan", width=5, command=lambda: self.build_formula('tan(x)'))
        self.tan.grid(row=1, column=2)
        self.sqrt = Button(self.frame, text="sqrt", width=5, command=lambda: self.build_formula('sqrt(x)'))
        self.sqrt.grid(row=2, column=0)
        self.exp = Button(self.frame, text="e", width=5, command=lambda: self.build_formula('exp(x)'))
        self.exp.grid(row=2, column=1)
        self.ln = Button(self.frame, text="ln", width=5, command=lambda: self.build_formula('ln(x)'))
        self.ln.grid(row=2, column=2)
        self.bracket_l = Button(self.frame, text="(", width=5, command=lambda: self.build_formula('('))
        self.bracket_l.grid(row=3, column=0)
        self.bracket_r = Button(self.frame, text=")", width=5, command=lambda: self.build_formula(')'))
        self.bracket_r.grid(row=3, column=1)
        self.comma = Button(self.frame, text=";", width=5, command=lambda: self.build_formula(';'))
        self.comma.grid(row=3, column=2)
        self.power = Button(self.frame, text="^", width=5, command=lambda: self.build_formula('**'))
        self.power.grid(row=4, column=2)
        self.plus = Button(self.frame, text="+", width=5, command=lambda: self.build_formula('+'))
        self.plus.grid(row=4, column=0)
        self.minus = Button(self.frame, text="-", width=5, command=lambda: self.build_formula('-'))
        self.minus.grid(row=4, column=1)
        self.divide = Button(self.frame, text="/", width=5, command=lambda: self.build_formula('/'))
        self.divide.grid(row=5, column=0)
        self.multiple = Button(self.frame, text="*", width=5, command=lambda: self.build_formula('*'))
        self.multiple.grid(row=5, column=1)
        self.clear = Button(self.frame, text="C", width=5, command=self.clear)
        self.clear.grid(row=5, column=2)

        self.range_axes_X = ttk.Label(self, text="Określ zakresy na osi X: ", borderwidth=10)
        self.range_axes_X.grid(row=7, column=0, pady=15)
        self.label_axes_X = ttk.Label(self, text="Wpisz nazwę dla osi X: ", borderwidth=10)
        self.label_axes_X.grid(row=8, column=0, pady=15)
        self.range_axes_X_entry_l = Entry(self)
        self.range_axes_X_entry_l.grid(row=7, column=1)
        self.range_axes_X_entry_r = Entry(self)
        self.range_axes_X_entry_r.grid(row=7, column=2)
        self.label_axes_X_entry = Entry(self)
        self.label_axes_X_entry.grid(row=8, column=1)

        self.range_axes_Y = ttk.Label(self, text="Określ zakresy na osi Y: ")
        self.range_axes_Y.grid(row=9, column=0, pady=15)
        self.label_axes_Y = ttk.Label(self, text="Wpisz nazwę dla osi Y: ", borderwidth=10)
        self.label_axes_Y.grid(row=10, column=0, pady=15)
        self.range_axes_Y_entry_l = Entry(self)
        self.range_axes_Y_entry_l.grid(row=9, column=1)
        self.range_axes_Y_entry_r = Entry(self)
        self.range_axes_Y_entry_r.grid(row=9, column=2)
        self.label_axes_Y_entry = Entry(self)
        self.label_axes_Y_entry.grid(row=10, column=1)

        self.title = ttk.Label(self, text="Podaj tytuł wykresu:")
        self.title.grid(row=11, column=0, pady=15)
        self.title_entry = Entry(self)
        self.title_entry.grid(row=11, column=1)

        self.draw_button = Button(self, text="Rysuj", command=self.draw, borderwidth=10)
        self.draw_button.grid(row=12, column=1)

        self.intVarCheckB = IntVar()
        self.legend = Checkbutton(self, text="Pokaż legendę", variable=self.intVarCheckB)
        self.legend.grid(row=13, column=0, rowspan=2, pady=15)

        self.exit_button = Button(self, text="Zakończ", command=quit, borderwidth=10)
        self.exit_button.grid(row=15, column=1)

    def clear(self):
        u"""Funkcja odpowiada za usunięcie już wpisanego tekstu do pola
        służącego do podania wzoru funkcji."""
        self.function_formula.delete(0, END)

    def build_formula(self, text):
        u"""Funkcja służy do budowania wzoru funkcji poprzez wprowadzanie
        operatorów widocznych na przyciskach."""
        self.entry_text = self.function_formula.get()
        self.function_formula.insert(len(self.entry_text), text)

    def draw(self):
        u"""Funkcja definuje czynnosc wykonywana po nacisnieciu przycisku "Rysuj"."
        Tworzy wykres na podstawie danych wprowadzonych przez uzytkownika."""

        self.f = Figure()
        self.a = self.f.add_subplot(111)
        title = self.title_entry.get()
        self.a.set_title(title)
        self.a.set_ylabel(self.label_axes_Y_entry.get(), fontsize=14)
        self.a.set_xlabel(self.label_axes_X_entry.get(), fontsize=14)
        self.canvas = FigureCanvasTkAgg(self.f, self)

        txt = re.split('[;,]', self.function_formula.get())

        x_values = np.linspace(eval(self.range_axes_X_entry_l.get()), eval(self.range_axes_X_entry_r.get()), 100)

        for fun in txt:
            y_values = np.zeros(100)
            for i in range(0, len(x_values)):
                y_values[i] = eval(fun, {'x': float(x_values[i]), 'sin': sin, 'cos': cos, 'tan': tan,
                                         'exp': exp, 'ln': log1p, 'sqrt': sqrt})

            if self.intVarCheckB == 1:
                self.a.plot(x_values, y_values, label=fun)
                self.a.axis([eval(self.range_axes_X_entry_l.get()), eval(self.range_axes_X_entry_r.get()),
                             eval(self.range_axes_Y_entry_l.get()), eval(self.range_axes_Y_entry_r.get())])

            else:
                self.a.plot(x_values, y_values, label=fun)
                self.a.axis([eval(self.range_axes_X_entry_l.get()), eval(self.range_axes_X_entry_r.get()),
                             eval(self.range_axes_Y_entry_l.get()), eval(self.range_axes_Y_entry_r.get())])

        if self.intVarCheckB.get() == 1:
            self.a.legend(loc='upper right', shadow=True)

        self.canvas.get_tk_widget().grid(row=0, column=5, rowspan=14, columnspan=6, sticky=N + S, padx=10)

        self.save_text = ttk.Label(self, text="Podaj nazwę pliku: ")
        self.save_text.grid(row=14, column=5)
        self.save = Entry(self)
        self.save.grid(row=14, column=6)
        self.save_button = Button(self, text="Zapisz do pliku png", command=self.save_plot, borderwidth=10)
        self.save_button.grid(row=14, column=7)

    def save_plot(self):
        u"""Funkcja służy do zapisania stworzonego wykresu w formacie png."""
        self.f.savefig(self.save.get() + '.png')
        self.save.delete(0, END)


root = Tk()
app = Plot(root)
app.mainloop()
