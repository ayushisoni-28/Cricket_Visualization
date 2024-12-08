from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb+srv://avinash:avinash@cluster0.ge32g.mongodb.net/')
db = client['rohit_data']

# Initialize the driver
driver = webdriver.Chrome()

# Open the URL
driver.get('https://www.espncricinfo.com/cricketers/rohit-sharma-34102/bowling-batting-stats')

# Function to extract and process tables for different formats
def extract_data(span_value, match_format):
    wait = WebDriverWait(driver, 10)
    span = wait.until(EC.presence_of_element_located((By.XPATH, f"//span[@class='ds-text-tight-m ds-font-regular ds-text-typo' and text()='{span_value}']")))
    
    # Click the tab corresponding to the format
    span.click()

    time.sleep(2)  # Wait for the page to load

    # Extract the page source and parse with BeautifulSoup
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    tables = soup.find_all('table')

    all_tables = []

    # Loop through the tables and convert them to DataFrames
    for table in tables:
        try:
            df = pd.read_html(str(table))[0]
            all_tables.append(df)
        except ValueError as e:
            print(f"Error processing table: {e}")

    # Ensure there are at least 6 tables
    if len(all_tables) >= 6:
        table_2 = all_tables[1]  # Table 2
        table_6 = all_tables[5]  # Table 6

        # Drop specified columns
        columns_to_drop = ['BF', '0s', '4s', '6s']
        table_2 = table_2.drop(columns=columns_to_drop)
        table_6 = table_6.drop(columns=columns_to_drop)

        # Clean up and rename columns
        table_2['Unnamed: 0'] = table_2['Unnamed: 0'].str.replace('vs', '')
        table_6['Unnamed: 0'] = table_6['Unnamed: 0'].str.replace('year', '')

        table_2.rename(columns={'Unnamed: 0': f'Rohit_{match_format}_Teams', 'Span': f'Rohit_{match_format}_Span', 'Mat': f'Rohit_{match_format}_Match',
                                'Inns': f'Rohit_{match_format}_Innings', 'NO': f'Rohit_{match_format}_NotOut', 'Runs': f'Rohit_{match_format}_Runs',
                                'HS': f'Rohit_{match_format}_HighestScore', 'Avg': f'Rohit_{match_format}_Average', 'SR': f'Rohit_{match_format}_StrikeRate',
                                '100s': f'Rohit_{match_format}_100s', '50s': f'Rohit_{match_format}_50s'}, inplace=True)

        table_6.rename(columns={'Unnamed: 0': f'Rohit_{match_format}Year', 'Mat': f'Rohit_{match_format}Year_Match', 'Inns': f'Rohit_{match_format}Year_Innings',
                                'NO': f'Rohit_{match_format}Year_NotOut', 'Runs': f'Rohit_{match_format}Year_Runs', 'HS': f'Rohit_{match_format}Year_HighestScore',
                                'Avg': f'Rohit_{match_format}Year_Average', 'SR': f'Rohit_{match_format}Year_StrikeRate', '100s': f'Rohit_{match_format}Year_100s',
                                '50s': f'Rohit_{match_format}Year_50s'}, inplace=True)

        return table_2, table_6
    else:
        print(f"Not enough tables extracted for {match_format}. Found:", len(all_tables))
        return None, None

# Function to store data into MongoDB
def store_data_in_mongo(collection_name, table_2, table_6):
    if table_2 is not None and table_6 is not None:
        # Convert the DataFrames to dictionaries
        table_2_records = table_2.to_dict('records')
        table_6_records = table_6.to_dict('records')

        # Store data in MongoDB
        db[collection_name].insert_many(table_2_records)
        db[collection_name].insert_many(table_6_records)
        print(f"Data inserted into MongoDB collection: {collection_name}")

# Extract data for Tests, ODIs, and T20Is
test_table_2, test_table_6 = extract_data('Tests', 'Test')
odi_table_2, odi_table_6 = extract_data('ODIs', 'ODI')
t20_table_2, t20_table_6 = extract_data('T20Is', 'T20')

# Close the driver
driver.quit()

# Store data into MongoDB
if test_table_2 is not None:
    store_data_in_mongo('rohit_test', test_table_2, test_table_6)
if odi_table_2 is not None:
    store_data_in_mongo('rohit_odi', odi_table_2, odi_table_6)
if t20_table_2 is not None:
    store_data_in_mongo('rohit_t20', t20_table_2, t20_table_6)

print("Data successfully stored in MongoDB.")
