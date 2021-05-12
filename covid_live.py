import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers
import numpy as np

from itertools import count
from collections import deque
import requests
import io
from IPython import display

from _utils import month_dict, api_url

state = "India"
year = 2021

api_response = requests.get(api_url).content
data = pd.read_csv(io.StringIO(api_response.decode('utf-8')))

cases = deque(np.zeros(8))
recov = deque(np.zeros(8))
deaths = deque(np.zeros(8))
tests = deque(np.zeros(8))

days = deque(np.zeros(8))
fig, axes = plt.subplots(2, 2, figsize=(12, 6))
index = count()


def create_daily(df, col):
    df[f"daily_{col}"] = pd.Series(np.zeros_like(df[col].values))
    for i in range(1, df.shape[0]):
        sub = df[col][i] - df[col][i-1]
        df[f"daily_{col}"].iloc[i] = sub

data_state = data[data.Date.str.startswith(str(year))]
data_state = data_state[data_state.State == state]
data_state = data_state.reset_index(drop=True)

create_daily(data_state, "Confirmed")
create_daily(data_state, "Recovered")
create_daily(data_state, "Deceased")


data_state = data_state.reset_index(drop=True)


create_daily(data_state, "Tested")
#print("3 index", np.unique(data_state.index), "\n total",  len(np.unique(data_state.index)))
data_state = data_state.drop([0, data_state.shape[0]-1])
#print("4 index", np.unique(data_state.index), "\n total",  len(np.unique(data_state.index)))
days_list = [f"{month_dict[date[5:7]]} {date[8:]}" for date in data_state.Date]

data_state = data_state.fillna(0)

cases_list = data_state.daily_Confirmed
recov_list = data_state.daily_Recovered
deaths_list = data_state.daily_Deceased
tests_list = data_state.daily_Tested


def update(i):
    if year == 20:
        fig.suptitle(f"Covid-19 analysis {state} - {year}20-21", fontsize=16)
    else:
        fig.suptitle(f"Covid-19 analysis {state} - {year}", fontsize=16)


    ind = next(index)

    print("current index", ind+1)

    days.popleft()
    days.append(days_list[ind+1])

    cases.popleft()
    cases.append(cases_list[ind+1])

    recov.popleft()
    recov.append(recov_list[ind+1])

    deaths.popleft()
    deaths.append(deaths_list[ind+1])

    tests.popleft()
    tests.append(tests_list[ind+1])

    axes[0][0].cla()
    axes[0][1].cla()
    axes[1][0].cla()
    axes[1][1].cla()

    axes[0][0].plot(days, cases)
    axes[0][0].scatter(len(cases) -1, cases[-1])
    axes[0][0].text(len(cases) - 1, cases[-2], "{}".format(cases[-1]), fontdict = {"fontsize" : 11})
    axes[0][0].set_xticklabels(days, fontdict={"fontsize": 7})
    axes[0][0].set_ylim(0, max(cases_list))
    axes[0][0].grid()

    axes[0][1].plot(days, recov, color="green")
    axes[0][1].scatter(len(recov) - 1, recov[-1], color ="green")
    axes[0][1].text(len(recov) - 1, recov[-2], "{}".format(recov[-1]), fontdict={"fontsize": 11})
    axes[0][1].set_xticklabels(days, fontdict={"fontsize": 7})
    axes[0][1].set_ylim(0, max(recov_list))
    axes[0][1].grid()

    axes[1][0].plot(days, deaths, color="red")
    axes[1][0].scatter(len(deaths) - 1, deaths[-1], color="red")
    axes[1][0].text(len(deaths) - 1, deaths[-2], "{}".format(deaths[-1]), fontdict={"fontsize": 11})
    axes[1][0].set_xticklabels(days, fontdict={"fontsize": 7})
    axes[1][0].set_ylim(0, max(deaths_list))
    axes[1][0].grid()

    axes[1][1].plot(days, tests, color="orange")
    axes[1][1].scatter(len(tests) - 1, tests[-1], color="orange")
    axes[1][1].text(len(tests) - 1, tests[-2], "{}".format(tests[-1]), fontdict={"fontsize": 11})
    axes[1][1].set_xticklabels(days, fontdict={"fontsize": 7})
    axes[1][1].set_ylim(0, max(tests_list))
    axes[1][1].grid()

    axes[0][0].set_title("Cases (Daily)", fontsize=9)
    axes[0][1].set_title("Recoveries (Daily)", fontsize=9)
    axes[1][0].set_title("Deaths (Daily)", fontsize=9)
    axes[1][1].set_title("Tests (Daily)", fontsize=9)



ani = FuncAnimation(fig, update, interval=500, frames = 440)
#Writer = writers["ffmpeg"]
#writer = Writer(fps=15, metadata={'artist': 'Me'}, bitrate=1800)

#ani.save('covid india 2021 4.mp4', writer)

plt.show()
