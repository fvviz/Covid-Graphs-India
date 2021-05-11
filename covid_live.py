import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from itertools import count
from collections import deque
import requests
import io

from _utils import month_dict, api_url

state = "India"
year = 2021

api_response = requests.get(api_url).content
data = pd.read_csv(io.StringIO(api_response.decode('utf-8')))

cases = deque(np.zeros(7))
recov = deque(np.zeros(7))
deaths = deque(np.zeros(7))
tests = deque(np.zeros(7))

days = deque(np.zeros(7))
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

cases_list = data_state.daily_Confirmed
recov_list = data_state.daily_Recovered
deaths_list = data_state.daily_Deceased
tests_list = data_state.daily_Tested


def update(i):
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
    axes[0][1].plot(days, recov, color="green")
    axes[1][0].plot(days, deaths, color="red")
    axes[1][1].plot(days, tests, color="orange")


axes[0][0].set_title("Cases (Daily)", fontsize=9)
axes[0][1].set_title("Recoveries (Daily)", fontsize=9)
axes[1][0].set_title("Deaths (Daily)", fontsize=9)
axes[1][1].set_title("Tests (Daily)", fontsize=9)

#print("4 made it til here")
ani = FuncAnimation(fig, update, interval=100)
#print("5 made it til here")
#print(data_state.head())
plt.show()
