import json
import requests
import time
import pandas as pd
import numpy as np
from inventory_definitions import *
from datetime import datetime, timedelta, time
from creds import weather_key_id

path = r'C:\Users\ikesu\Uncle Ikes\Onedrive Admin - Uncle Ikes Accounting\ISAAC\3. Monthly Reconciliation Stuff\Tableau Project\Weather Data'
second_path = r"C:\Users\ikesu\Documents\Tableau Project\Weather Data"
main_master = r'C:\Users\ikesu\Uncle Ikes\Onedrive Admin - Uncle Ikes Accounting\ISAAC\3. Monthly Reconciliation Stuff\Tableau Project\Weather Data\Main Weather Master.csv'
second_master = r'C:\Users\ikesu\Uncle Ikes\Onedrive Admin - Uncle Ikes Accounting\ISAAC\3. Monthly Reconciliation Stuff\Tableau Project\Weather Data\Secondary Weather Master.csv'
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)


def weather_api(day_unix_time, day_date):
    # Call API from OpenWeatherMap.org
    url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=47.6062&lon=-122.3321&dt={day_unix_time}&units=imperial&appid={weather_key_id}'
    r = requests.get(url)
    weather_dict = json.loads(r.content)

    # Combine Weather API Dictionaries into DataFrame
    df = pd.json_normalize(weather_dict)
    df1 = pd.DataFrame(df['hourly'].values.tolist()
                       ).add_prefix('hourly.')

    df_list = list()
    for (columnName, columnData) in df1.iteritems():
        huh = columnData.values.tolist()
        df2 = pd.DataFrame.from_dict(huh)
        df_list.append(df2)

    # Format Hourly DataFrame
    df_hourly = pd.concat(df_list)
    df_hourly = df_hourly.reset_index()

    # Format Weather DataFrame (For Main)
    df_weather = pd.json_normalize(
        weather_dict['hourly'], record_path='weather', meta='dt')
    df_weather = df_weather.drop_duplicates(
        subset='dt', keep='first').reset_index(drop=True)

    # Combine DataFrames
    df_combined = df_hourly.drop(['weather'], axis=1).merge(
        df_weather, left_on='dt', right_on='dt', how='outer')

    # Add Datetime Columns
    df_combined['Datetime'] = (pd.to_datetime(df_combined['dt'], unit='s'))
    df_combined['Date'] = pd.to_datetime(df_combined['Datetime']).dt.date
    df_combined['Time'] = pd.to_datetime(df_combined['Datetime']).dt.time

    # Format Rain Column
    if 'rain' in df_combined.columns:
        df_combined[['delete', 'rain2']] = df_combined['rain'].apply(pd.Series)
        df_combined = df_combined.drop(
            ['delete', 'rain'], axis=1)

        # Rename Columns (With Rain)
        df_combined.rename(columns={'dt': 'DT', 'temp': 'Temp(F)', 'feels_like': 'Feels Like(F)', 'pressure': 'Pressure(hPa)', 'humidity': 'Humidity(%)', 'dew_point': 'Dew Point(F)', 'uvi': 'UVI', 'clouds': 'Clouds(%)', 'visibility': 'Visibility(Metres)',
                                    'wind_speed': 'Wind Speed(MPH)', 'wind_deg': 'Wind Degree', 'wind_gust': 'Wind Gust(MPH)', 'rain2': 'Rain 1HR(MM)', 'id': 'Weather ID', 'main': 'Main Weather', 'description': 'Weather Description'}, inplace=True)

        df_combined = df_combined[['Date', 'Time', 'DT', 'Temp(F)', 'Feels Like(F)', 'Pressure(hPa)', 'Humidity(%)', 'Dew Point(F)', 'UVI', 'Clouds(%)',
                                   'Visibility(Metres)', 'Wind Speed(MPH)', 'Wind Degree', 'Wind Gust(MPH)', 'Rain 1HR(MM)', 'Main Weather', 'Weather Description']]
    else:
        # Rename Columns (No Rain)

        df_combined.rename(columns={'dt': 'DT', 'temp': 'Temp(F)', 'feels_like': 'Feels Like(F)', 'pressure': 'Pressure(hPa)', 'humidity': 'Humidity(%)', 'dew_point': 'Dew Point(F)', 'uvi': 'UVI', 'clouds': 'Clouds(%)', 'visibility': 'Visibility(Metres)',
                                    'wind_speed': 'Wind Speed(MPH)', 'wind_deg': 'Wind Degree', 'wind_gust': 'Wind Gust(MPH)', 'id': 'Weather ID', 'main': 'Main Weather', 'description': 'Weather Description'}, inplace=True)

        df_combined = df_combined[['Date', 'Time', 'DT', 'Temp(F)', 'Feels Like(F)', 'Pressure(hPa)', 'Humidity(%)', 'Dew Point(F)', 'UVI', 'Clouds(%)',
                                   'Visibility(Metres)', 'Wind Speed(MPH)', 'Wind Degree', 'Wind Gust(MPH)', 'Main Weather', 'Weather Description']]

    # Create Averages DataFrames
    means = df_combined.mean(numeric_only=True, axis=0).round(decimals=2)
    df_total = pd.DataFrame(means).transpose().add_prefix(
        'Avg ')
    df_total['Date'] = df_combined['Date'].iat[-1]
    df_total['Max Temp(F)'] = df_combined['Temp(F)'].max(axis=0)
    df_total['Min Temp(F)'] = df_combined['Temp(F)'].min(axis=0)

    # Format Total Dataframe
    if 'Rain 1HR(MM)' in df_combined.columns:
        df_total['Total Rain(MM)'] = df_combined['Rain 1HR(MM)'].sum(axis=0)
        df_total['Avg Rain(MM)'] = df_total['Total Rain(MM)'] / 12
        df_total['Avg Rain(MM)'] = df_total['Avg Rain(MM)'].round(2)
        print('Rain Exists')
        df_total = df_total[['Date', 'Max Temp(F)', 'Min Temp(F)', 'Avg Temp(F)', 'Avg Feels Like(F)', 'Total Rain(MM)', 'Avg Rain(MM)', 'Avg Pressure(hPa)', 'Avg Humidity(%)', 'Avg Dew Point(F)',
                            'Avg UVI', 'Avg Clouds(%)', 'Avg Visibility(Metres)', 'Avg Wind Speed(MPH)', 'Avg Wind Degree', 'Avg Wind Gust(MPH)']]
    else:
        print('Rain Does Not Exists')
        df_total['Total Rain(MM)'] = 0
        df_total['Avg Rain(MM)'] = 0
        df_total = df_total[['Date', 'Max Temp(F)', 'Min Temp(F)', 'Avg Temp(F)', 'Avg Feels Like(F)', 'Total Rain(MM)', 'Avg Rain(MM)', 'Avg Pressure(hPa)', 'Avg Humidity(%)', 'Avg Dew Point(F)',
                            'Avg UVI', 'Avg Clouds(%)', 'Avg Visibility(Metres)', 'Avg Wind Speed(MPH)', 'Avg Wind Degree', 'Avg Wind Gust(MPH)']]

    # Sort Weather Descriptors into List
    weather1_list = list(
        df_combined['Weather Description'].values.ravel())

    weather2 = []
    for i in weather1_list:
        if i not in weather2:
            weather2.append(i)
    weather2.sort()

    # Create Weather DataFrame (For More Detailed)
    df_weather2 = pd.DataFrame()
    df_weather2['Main Weather'] = weather2
    df_weather2['Date'] = df_combined['Date'].iat[-1]
    df_weather2 = df_weather2[['Date', 'Main Weather']]

    # Write to Excel
    writer = pd.ExcelWriter(
        '{}/{}.xlsx'.format(path, day_date+' Weather Data'), engine="xlsxwriter")
    df_combined.to_excel(writer, "All", index=None)
    df_total.to_excel(writer, sheet_name='Totals', index=None)
    df_weather2.to_excel(writer, sheet_name='Weather', index=None)
    writer.save()

    # Write to CSV
    df_total.to_csv(main_master, mode='a', index=False, header=False)
    df_weather2.to_csv(second_master, mode='a', index=False, header=False)


yesterday_tuple = (yesterday_unix_time, yesterday_weather_date)
two_tuple = (two_days_unix_time, two_days_weather_date)
three_tuple = (three_days_unix_time, three_days_weather_date)
four_tuple = (four_days_unix_time, four_days_weather_date)
five_tuple = (five_days_unix_time, five_days_weather_date)


weather_api(*(yesterday_tuple))
