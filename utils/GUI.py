from tkinter import *
import tkinter.ttk
from collections import deque
from itertools import count
import numpy as np

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from utils._utils import get_state_data
from utils.constants import state_options, year_options


class GUI(Tk):
    def __init__(self, graph_interval, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Covid-19 India live graph")
        self.configure(bg="gray")
        self.geometry("1300x800")

        self.state_selected = StringVar()
        self.state_selected.set("All states")
        state_drop = OptionMenu(self, self.state_selected, *state_options)
        state_drop.config(width=10, height =1)
        state_drop.place(x=5, y=250)

        self.year_selected = StringVar()
        self.year_selected.set("2021")
        year_drop = OptionMenu(self, self.year_selected, *year_options)
        year_drop.config(width=10, height=1)
        year_drop.place(x=5, y=300)

        self.start_button = Button(self, text = "Start",  command = self.start, height=3, width=20)
        self.start_button.place(x=550,y=700)

        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().place(x=150, y=80)

    def start(self):
        cases = deque(np.zeros(8))
        recov = deque(np.zeros(8))
        deaths = deque(np.zeros(8))
        tests = deque(np.zeros(8))

        days = deque(np.zeros(8))
        index = count()

        year = self.year_selected.get()
        state = "India" if self.state_selected.get() == "All states" else self.state_selected.get()

        cases_list, recov_list, deaths_list, tests_list, days_list = get_state_data(state, year)

        def update(i):
            if year == "2020-21":
                self.fig.suptitle(f"Covid-19 analysis {state} - {year}", fontsize=16)
            else:
                self.fig.suptitle(f"Covid-19 analysis {state} - {year}", fontsize=16)

            ind = next(index)
            print("current index", ind + 1)

            days.popleft()
            days.append(days_list[ind + 1])

            cases.popleft()
            cases.append(cases_list[ind + 1])

            recov.popleft()
            recov.append(recov_list[ind + 1])

            deaths.popleft()
            deaths.append(deaths_list[ind + 1])

            tests.popleft()
            tests.append(tests_list[ind + 1])

            self.axes[0][0].cla()
            self.axes[0][1].cla()
            self.axes[1][0].cla()
            self.axes[1][1].cla()

            self.axes[0][0].plot(days, cases)
            self.axes[0][0].scatter(len(cases) - 1, cases[-1])
            self.axes[0][0].text(len(cases) - 1, cases[-2], "{}".format(cases[-1]), fontdict={"fontsize": 11})
            self.axes[0][0].set_xticklabels(days, fontdict={"fontsize": 7})
            self.axes[0][0].set_ylim(0, max(cases_list))
            self.axes[0][0].grid()

            self.axes[0][1].plot(days, recov, color="green")
            self.axes[0][1].scatter(len(recov) - 1, recov[-1], color="green")
            self.axes[0][1].text(len(recov) - 1, recov[-2], "{}".format(recov[-1]), fontdict={"fontsize": 11})
            self.axes[0][1].set_xticklabels(days, fontdict={"fontsize": 7})
            self.axes[0][1].set_ylim(0, max(recov_list))
            self.axes[0][1].grid()

            self.axes[1][0].plot(days, deaths, color="red")
            self.axes[1][0].scatter(len(deaths) - 1, deaths[-1], color="red")
            self.axes[1][0].text(len(deaths) - 1, deaths[-2], "{}".format(deaths[-1]), fontdict={"fontsize": 11})
            self.axes[1][0].set_xticklabels(days, fontdict={"fontsize": 7})
            self.axes[1][0].set_ylim(0, max(deaths_list))
            self.axes[1][0].grid()

            self.axes[1][1].plot(days, tests, color="orange")
            self.axes[1][1].scatter(len(tests) - 1, tests[-1], color="orange")
            self.axes[1][1].text(len(tests) - 1, tests[-2], "{}".format(tests[-1]), fontdict={"fontsize": 11})
            self.axes[1][1].set_xticklabels(days, fontdict={"fontsize": 7})
            self.axes[1][1].set_ylim(0, max(tests_list))
            self.axes[1][1].grid()

            self.axes[0][0].set_title("Cases (Daily)", fontsize=9)
            self.axes[0][1].set_title("Recoveries (Daily)", fontsize=9)
            self.axes[1][0].set_title("Deaths (Daily)", fontsize=9)
            self.axes[1][1].set_title("Tests (Daily)", fontsize=9)


        #canvas.get_tk_widget().place(x=500, y=5)

        ani = FuncAnimation(self.fig, update, interval=100, frames=1000)
        self.canvas.draw()


