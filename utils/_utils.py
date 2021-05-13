import pandas as pd
import numpy as np

import requests
import io

from utils.constants import api_url, month_dict


def get_data():
    api_response = requests.get(api_url).content
    data = pd.read_csv(io.StringIO(api_response.decode('utf-8')))
    return data


def create_daily(df, col):
    df[f"daily_{col}"] = pd.Series(np.zeros_like(df[col].values))
    for i in range(1, df.shape[0]):
        sub = df[col][i] - df[col][i-1]
        df[f"daily_{col}"].iloc[i] = sub


def get_state_data(state, year):
    data = get_data()
    data_state = data[data.Date.str.startswith(str(year))]
    data_state = data_state[data_state.State == state]
    data_state = data_state.reset_index(drop=True)

    create_daily(data_state, "Confirmed")
    create_daily(data_state, "Recovered")
    create_daily(data_state, "Deceased")

    data_state = data_state.reset_index(drop=True)
    create_daily(data_state, "Tested")
    data_state = data_state.drop([0, data_state.shape[0]-1])
    data_state = data_state.fillna(0)

    cases_list = data_state.daily_Confirmed
    recov_list = data_state.daily_Recovered
    deaths_list = data_state.daily_Deceased
    tests_list = data_state.daily_Tested
    days_list = [f"{month_dict[date[5:7]]} {date[8:]}" for date in data_state.Date]

    return cases_list, recov_list, deaths_list, tests_list , days_list