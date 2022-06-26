from time import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from prophet import Prophet
from tqdm import tqdm
import requests


def main():
    file_name = "Testdaten.xlsx"
    split_date = '04-Jul_2022'
    days_to_forecast = 7
    timestamp_column = 'timestamp_new'
    value_column = 'personCount'
    middleware_url = "https://fa-roomitor.azurewebsites.net/api/predictions"
    middleware_api_key = "VOXG7U915GhnWo1dRCd-wuNrhgM897uDp4Lae4-kTKZCAzFu7O0DIA=="
    deviceID = "2187733e6049fabe904a1a730fe7c457"
    measurementName = "personCount"
    roomName = "A457"
    data = pd.read_excel(file_name)
    grouped_data = create_new_dataframe_grouped_with_index(data, timestamp_column, value_column)
    train_data, test_data = split_data(grouped_data, split_date)
    model = Prophet()
    train_model(model, train_data, timestamp_column, value_column)
    predicted_values = predict_values(model, days=days_to_forecast)
    upload_predictions(predicted_values[['ds', 'yhat']], deviceID, measurementName, roomName, middleware_url, middleware_api_key)


def create_new_dataframe_grouped_with_index(dataframe, timestamp_column, value_column):
    dataframe_modified = dataframe[[timestamp_column, value_column]]
    dataframe_modified[timestamp_column] = pd.to_datetime(dataframe_modified[timestamp_column], errors='coerce')
    dataframe_modified = dataframe_modified.groupby([dataframe_modified[timestamp_column].dt.month, dataframe_modified[timestamp_column].dt.day, dataframe_modified[timestamp_column].dt.hour])[value_column].mean()
    new_list = []
    for index, value in dataframe_modified.items():
        new_dataframe_row = {timestamp_column: datetime.strptime(f"2022-{index[0]}-{index[1]} {index[2]}:00:00", "%Y-%m-%d %H:%M:%S"), value_column: value}
        new_list.append(new_dataframe_row)
    new_dataframe = pd.DataFrame.from_records(new_list, columns=[timestamp_column, value_column])
    new_dataframe = new_dataframe.set_index(timestamp_column)
    return new_dataframe

def split_data(dataframe, split_date):
    split_date = '03-Jul-2022'
    train_data = dataframe.loc[dataframe.index <= split_date].copy()
    test_data = dataframe.loc[dataframe.index > split_date].copy()
    return train_data, test_data


def train_model(model, train_data, timestamp_column, value_column):
    model.fit(train_data.reset_index()
              .rename(columns={timestamp_column: 'ds',
                               value_column: 'y'}))


def predict_values(model, days=7):
    future_dataframe = model.make_future_dataframe(periods=days*24, freq="H", include_history=False)
    predictions = model.predict(future_dataframe)
    return predictions


def upload_predictions(predictions, deviceID, measurementName, roomName, middleware_url, middleware_api_key):
    print(predictions.head())
    return None
    for _, row in tqdm(predictions.iterrows(), total=predictions.shape[0]):
        data = {
            "deviceID": deviceID,
            "measurementName": measurementName,
            "measurementValue": row["yhat"],
            "timestamp": row["ds"].strftime("%Y-%m-%d %H:%M:%S"),
            "roomName": roomName
        }
        requests.post(middleware_url+"?code="+middleware_api_key, json=data)


if __name__ == '__main__':
    main()
