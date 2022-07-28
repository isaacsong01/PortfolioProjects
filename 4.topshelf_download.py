import time
import shutil
import pandas as pd
import xlwings as xw
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from creds import tshelf_username, tshelf_password
from daily_definitions import *
appended_data = []

cd_tuple = (cd_location, cd_topshelf, appended_data)
ch_tuple = (ch_location, ch_topshelf, appended_data)
lc_tuple = (lc_location, lc_topshelf, appended_data)
ow_tuple = (ow_location, ow_topshelf, appended_data)
wc_tuple = (wc_location, wc_topshelf, appended_data)


def chrome_stuff(topshelf_temp_path):
    global driver
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': topshelf_temp_path}
    options.add_experimental_option('prefs', prefs)
    s = Service(
        r"C:\Users\ikesu\AppData\Local\Microsoft\WindowsApps\chromedriver")
    driver = webdriver.Chrome(options=options, service=s)

    file_url = "https://www.topshelfdata.com"
    driver.get(file_url)

    # Login TopShelf Data
    driver.find_element(
        By.XPATH, '//*[@id="header"]/div[2]/div/span/a[6]').click()

    # Input Username and Password
    username = driver.find_element(
        By.XPATH, '/html/body/div[8]/div/div/div/form/p[1]/input')
    username.send_keys(tshelf_username)

    driver.find_element(
        By.XPATH, '//*[@id="password"]').send_keys(tshelf_password)
    driver.find_element(
        By.XPATH, '//*[@id="sign_in_form"]/p[3]/button').click()


def drag_and_drop(driver, source, target=None, offsetX=0, offsetY=0, delay=25, key=None):
    driver.execute_script(JS_DRAG_AND_DROP, source,
                          target, offsetX, offsetY, delay, key)
    time.sleep(delay * 2 / 1000)


def grab_csv_info(store, store_option, appended_data):
    # Go to Specific Venue
    driver.find_element(By.XPATH, '//*[@id="company_id"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, store_option).click()
    time.sleep(4)

    # Source Table to DataFrame
    source = driver.page_source
    df_list = pd.read_html(source)
    df = df_list[1]
    df.reset_index()

    # Create Columns
    df.columns = ['delete', 'Vendor', 'Category', 'Flower Type', 'Product Name', 'Package Size', 'Price Tier', 'Brand', 'Strain', 'Avg Wholesale Cost', 'Avg Retail Price',
                  'Avg Markup with Tax', 'Units on Hand', 'Sales last 7 days', 'Sales 2 weeks ago', 'Sales 3 weeks agp', 'Sales 4 weeks ago', '28 Day Unit Sales', 'Avg Daily Unit Sales', 'Days Supply Left', 'Supply %', 'Units Needed']
    df.drop('delete', inplace=True, axis=1)
    df.insert(0, 'Location', pd.Series(store))
    df['Location'] = df['Location'].ffill()
    pd.set_option('display.max_columns', None)

    # Format Numbers
    #special_chars = '$-(),%'
    def char_replace(s):
        for special_char in ['$', '-', '(', ')', ',', '%']:
            s = s.replace(special_char, '')
        return s
    # Replace Special Characters
    df['Avg Wholesale Cost'] = df['Avg Wholesale Cost'].map(char_replace)
    df['Avg Retail Price'] = df['Avg Retail Price'].map(char_replace)
    df['Supply %'] = df['Supply %'].map(char_replace)

    # Change Some Column Dtype to Float
    df.iloc[:, [9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]].astype(float)
    df['Supply %'] = df['Supply %'].astype(float)
    df['Supply %'] = df['Supply %'] * .01

    # Append Data to Dictionary
    appended_data.append(df)


def download_topshelf_report():
    try:
        # Date Definitions
        today_date = today.strftime('%m.%d.%y')

        chrome_stuff(topshelf_temp_path)
        # Go To Retailers Tab
        time.sleep(2)
        driver.find_element(
            By.XPATH, '//*[@id="header"]/div[2]/div/span/a[2]').click()
        time.sleep(2)

        # Move to Options Sub-Menu
        options = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="content"]/div[3]/div/div[1]/div[2]/a[3]')))
        options.click()
        time.sleep(1)

        select_show_data = Select(driver.find_element(By.ID, 'display_view'))
        select_show_data.select_by_visible_text('Table')
        time.sleep(1)

        select_supply_days = Select(
            driver.find_element(By.ID, 'target_supply_days'))
        select_supply_days.select_by_value('28')
        time.sleep(1)

        # Close Options Sub-Menu
        driver.find_element(
            By.XPATH, '//*[@id="dialog_display_options_container"]/a').click()
        time.sleep(10)
        driver.implicitly_wait(10)

        # Go to Group By Sub-Menu
        group_by = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="content"]/div[3]/div/div[1]/div[2]/a[1]')))
        group_by.click()
        time.sleep(2)

        group_list = ['flower_type', 'name', 'weight',
                      'flower_price_bin', 'brand', 'strain']

        # Drag and Drop
        for group in group_list:
            source_element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, group)))
            dest_element = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="group_by_columns"]')))
            drag_and_drop(driver, source_element, dest_element)
            time.sleep(2)

        # Reorder Columns
        vendor = 'vendor'
        product_type = 'product_type'
        flower_type = 'flower_type'
        name = 'name'
        weight = 'weight'
        flower_price_bin = 'flower_price_bin'
        brand = 'brand'
        strain = 'strain'

        position1 = driver.find_element(By.ID, vendor)
        position2 = driver.find_element(By.ID, product_type)
        position3 = driver.find_element(By.ID, flower_type)
        position4 = driver.find_element(By.ID, name)
        position5 = driver.find_element(By.ID, weight)
        position6 = driver.find_element(By.ID, flower_price_bin)
        position7 = driver.find_element(By.ID, brand)
        position8 = driver.find_element(By.ID, strain)

        drag_and_drop(driver, position1, position3)
        time.sleep(1)
        drag_and_drop(driver, position2, position3)
        time.sleep(1)
        drag_and_drop(driver, position4, position5)
        time.sleep(1)
        drag_and_drop(driver, position6, position7)
        time.sleep(1)

        # Close Group By Sub-Menu
        driver.find_element(
            By.XPATH, '//*[@id="dialog_group_by_container"]/a').click()
        time.sleep(5)

        # Compile DataFrames for Each Store Location
        location_tuple_list = [cd_tuple, ch_tuple,
                               lc_tuple, ow_tuple, wc_tuple]

        for location in location_tuple_list:
            grab_csv_info(*(location))
        df_combined = pd.concat(appended_data)

        # Write to CSV
        writer = pd.ExcelWriter(
            '{}/{}.xlsx'.format(topshelf_temp_path, 'TopShelf Cheat Sheet ' + today_date), engine="xlsxwriter")
        df_combined.to_excel(writer)
        writer.save()

        # Write to Excel using XLWings
        # xw.App().visible = False
        # wb = xw.Book(top_shelf_template)
        # ws = wb.sheets['Data']

        # ws['A2'].options(pd.DataFrame, header=1, index=True,
        #                  expand='table').value = df_combined

        # # If formatting of column names and index is needed as xlsxwriter does it, the following lines will do it.
        # ws["A2"].expand("right").api.Font.Bold = True
        # ws["A2"].expand("down").api.Font.Bold = True
        # ws["A2"].expand("right").api.Borders.Weight = 2
        # ws["A2"].expand("down").api.Borders.Weight = 2

        # wb.save('{}/{}.xlsx'.format(topshelf_temp_path,
        #         'TopShelf Cheat Sheet ' + today_date + ' 2'))
        # wb.close()
        # time.sleep(1)
        # print('Saved')

        # # Move Files to New Path
        # old_path = topshelf_temp_path + '\\' + \
        #     'TopShelf Cheat Sheet ' + today_date + '.xlsx'
        # new_path = topshelf_path
        # shutil.move(old_path, new_path)
        # print('Moved to New Path')

    except Exception as e:
        print(e, 'Not Working')

    time.sleep(1)
    driver.quit()


download_topshelf_report()
