import os
import time
import openpyxl
import pandas as pd
from datetime import timedelta, datetime
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from openpyxl.styles import Alignment
from creds import pb_username, pb_password
from daily_definitions import *


def webscrape_daily_sales(location_file, location_daily, location, which_option, which_days):
    try:
        global driver
        s = Service(
            r"C:\Users\ikesu\AppData\Local\Microsoft\WindowsApps\chromedriver")
        driver = webdriver.Chrome(service=s)

        # Which Website
        file_url = "https://app.posabit.com/login"
        driver.get(file_url)

        # Login to POSaBit
        driver.find_element(
            By.XPATH, '//*[@id="user_email"]').send_keys(pb_username)

        driver.find_element(
            By.XPATH, '//*[@id="user_password"]').send_keys(pb_password)
        driver.find_element(
            By.XPATH, '//*[@id="new_user"]/div[3]/input').click()

        # Click on which location
        driver.find_element(By.XPATH, '(//*[@id="navbarDropdown"])[3]').click()
        driver.find_element(
            By.XPATH, '//*[@id="wrapper"]/div[1]/nav/div/div/ul[1]/li[5]/ul/a[2]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, location).click()

        # Select the date
        time.sleep(2)
        select = Select(driver.find_element(By.ID, 'interval'))
        select.select_by_value(which_option)
        time.sleep(1)

        date_formatted = which_days.replace(
            hour=0, minute=0, second=0, microsecond=0)

        date_printed = which_days.strftime('%m/%d/%y')

        if which_option == '3':
            start_date = date_formatted + ' 12:00:00 AM'
            end_date = date_formatted + ' 11:59:59 PM'
            # Start Date Selection
            start_option = driver.find_element(
                By.XPATH, '//*[@id="start_time"]')
            start_option.send_keys(Keys.CONTROL + "a")
            start_option.send_keys(Keys.DELETE)
            time.sleep(1)
            start_option.send_keys(start_date)

            # End Date Selection
            end_option = driver.find_element(By.XPATH, '//*[@id="end_time"]')
            end_option.send_keys(Keys.CONTROL + "a")
            end_option.send_keys(Keys.DELETE)
            time.sleep(1)
            end_option.send_keys(end_date)

            # Click Option
            driver.find_element(
                By.XPATH, '//*[@id="filter"]/div/div/div[2]/button').click()

        else:
            # Click Option
            driver.find_element(
                By.XPATH, '//*[@id="filter"]/div/div/div[2]/button').click()

        # Grab data from table
        source = driver.page_source
        df_list = pd.read_html(source)
        df = df_list[0]
        df2 = df_list[1]

        daily_mj_sales_unedited = df['Net Sales'].values[0]
        daily_para_sales_unedited = df['Net Sales'].values[3]
        debit_count_unedited = df2['Tx Count (% Sales)'].values[2]
        debit_total_unedited = df2['Total Tendered'].values[2]
        debit_tip_unedited = df2['Gratuity'].values[2]
        debit_change_unedited = df2['Net Sales'].values[1]

        daily_unknown_unedited_test = df['Product Kind'].iloc[-2]
        daily_unknown_unedited = None
        if daily_unknown_unedited_test == 'Unknown':
            daily_unknown_unedited = df['Net Sales'].values[4]
            print('Unknown Exists')
        else:
            pass
            print('Unknown Doesnt Exist')

        # Format Values
        debit_count_unedited2 = debit_count_unedited.split('(')[0]
        special_chars = '$-(),%'
        for special_char in special_chars:
            daily_mj_sales_unedited = daily_mj_sales_unedited.replace(
                special_char, '')
            daily_para_sales_unedited = daily_para_sales_unedited.replace(
                special_char, '')
            debit_count_unedited2 = debit_count_unedited2.replace(
                special_char, '')
            debit_total_unedited = debit_total_unedited.replace(
                special_char, '')
            debit_tip_unedited = debit_tip_unedited.replace(special_char, '')
            debit_change_unedited = debit_change_unedited.replace(
                special_char, '')
            if daily_unknown_unedited is not None:
                daily_unknown_unedited = daily_unknown_unedited.replace(
                    special_char, '')
                daily_unknown = float(daily_unknown_unedited)
            else:
                pass

        daily_mj_sales = float(daily_mj_sales_unedited)
        daily_para_sales = float(daily_para_sales_unedited)
        debit_count = float(debit_count_unedited2)
        debit_total = float(debit_total_unedited)
        debit_tip = float(debit_tip_unedited)
        debit_change = float(debit_change_unedited)

        if daily_unknown_unedited is not None:
            print('Unknown Exists but not added')
        else:
            pass
            print('MJ Sales Only')

        # Add info into Daily Sales Spreadsheet
        wb = openpyxl.load_workbook(location_file)
        ws_sales = wb['SALES']
        ws_posabit = wb['POSABIT']

        for row in range(1, ws_sales.max_row+1):
            if ws_sales.cell(row=row, column=1).value == date_formatted:
                print('Found')
                ws_sales.cell(column=2, row=row, value=daily_mj_sales)
                ws_sales.cell(column=3, row=row, value=daily_para_sales)

        for row in range(1, ws_posabit.max_row+1):
            if ws_posabit.cell(row=row, column=1).value == date_formatted:
                print('Found')
                ws_posabit.cell(column=2, row=row, value=debit_count)
                ws_posabit.cell(column=3, row=row, value=debit_total)
                ws_posabit.cell(column=4, row=row, value=debit_tip)
                ws_posabit.cell(column=6, row=row, value=debit_change)

        # Format Worksheet
        for row in ws_posabit.iter_rows(min_row=3, min_col=2, max_col=2):
            for cell in row:
                cell.alignment = Alignment(
                    horizontal='center', vertical='center')

        max_row = len(ws_posabit['C'])
        for row in range(1, max_row+1):
            ws_posabit["C{}".format(
                row)].number_format = '#,##0.00_);(#,##0.00)'
            ws_posabit["D{}".format(
                row)].number_format = '#,##0.00_);(#,##0.00)'
            ws_posabit["F{}".format(
                row)].number_format = '#,##0.00_);(#,##0.00)'

        wb.save(location_file)

    except Exception as e:
        print(e, 'Not Working')

    time.sleep(1)
    driver.quit()


def open_sales(location_file, location_daily, location, which_option, which_days):
    os.startfile(location_file)


def open_daily(location_file, location_daily, location, which_option, which_days):
    os.startfile(location_daily)


cd_tuple = (cd_file, cd_daily, cd_posabit, yesterday_option, yesterday)
ch_tuple = (ch_file, ch_daily, ch_posabit, yesterday_option, yesterday)
lc_tuple = (lc_file, lc_daily, lc_posabit, yesterday_option, yesterday)
ow_tuple = (ow_file, ow_daily, ow_posabit, yesterday_option, yesterday)
wc_tuple = (wc_file, wc_daily, wc_posabit, yesterday_option, yesterday)

tuple_list = (cd_tuple, ch_tuple, lc_tuple, ow_tuple, wc_tuple)


def daily_sales(tuple_list):
    for tuple in tuple_list:
        # webscrape_daily_sales(*(tuple))
        open_sales(*(tuple))
        # open_daily(*(tuple))


daily_sales(tuple_list)

# open_sales(*(lc_tuple))
# open_daily(*(lc_tuple))
