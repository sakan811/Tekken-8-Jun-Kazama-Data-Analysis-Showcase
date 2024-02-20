import re

from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

urls = []
driver = webdriver.Chrome()
url = 'https://tekken8framedata.com/'
driver.get(url)

main_page_contents = driver.page_source
driver.close()
soup = BeautifulSoup(main_page_contents, 'html.parser')

pattern = re.compile(r'tekken-8-frame-data')
char_urls = soup.find_all('a', href=pattern)
char_url_list = [char_url['href'] for char_url in char_urls]
char_url_list = list(set(char_url_list))

for char_url in char_url_list:
    driver = webdriver.Chrome()
    driver.get(char_url)
    first_page_content = driver.page_source
    char_name = char_url.split("/")[-2]

    page_contents = [first_page_content]

    while True:
        # Capture the current page source before clicking the next button
        current_page_source = driver.page_source

        try:
            next_page_element = driver.find_element(By.XPATH, '//*[@id="tablesome__container"]/nav/ul/li[6]')
            next_page_element.click()

            # Capture the new page source after clicking the button
            new_page_source = driver.page_source

            # If the page content hasn't changed (indicating end of pagination), break the loop
            if current_page_source == new_page_source:
                print("No more dynamically changing pages found. Exiting loop.")
                break

            # Append the new page source to the list of page_contents
            page_contents.append(new_page_source)
        except NoSuchElementException:
            print("Next button element not found. Exiting loop.")
            break

    driver.quit()

    columns = {
        'Command': [],
        'Hit level': [],
        'Damage': [],
        'Startup': [],
        'Block': [],
        'Hit': [],
        'Counter Hit': [],
        'Notes': []
    }

    for content in page_contents:
        soup = BeautifulSoup(content, 'html.parser')

        column_names = soup.find_all('th', class_='tablesome__column svelte-1a34s8p')
        elements = soup.find_all('td', class_='tablesome__cell tablesome__cell--text')

        for i, element in enumerate(elements):
            j = i % 8  # Calculate column index

            if j == 0:
                columns['Command'].append(element.text)
            elif j == 1:
                columns['Hit level'].append(element.text)
            elif j == 2:
                if element.text == '-' or element.text == '?':
                    columns['Damage'].append(element.text)
                else:
                    # Extract numerical values using regular expression
                    damage_values = re.findall(r'\d+', element.text)
                    # Convert the extracted values to integers
                    damage_integers = [int(value) for value in damage_values]
                    columns['Damage'].append(sum(damage_integers))
            elif j == 3:
                match = re.match(r'\d+[?~]?\d*', str(element.text))
                if element.text == '-':
                    columns['Startup'].append(element.text)
                elif match:
                    # Use regular expression to extract the first integer
                    first_int = int(re.search(r'\d+', match.group()).group())
                    columns['Startup'].append(first_int)
                elif element.text.isdigit():
                    # Check if the text consists of digits only
                    columns['Startup'].append(int(element.text))
                else:
                    # Handle other cases, such as non-numeric values
                    columns['Startup'].append(None)
            elif j == 4:
                columns['Block'].append(element.text)
            elif j == 5:
                columns['Hit'].append(element.text)
            elif j == 6:
                columns['Counter Hit'].append(element.text)
            elif j == 7:
                columns['Notes'].append(element.text)

    df = pd.DataFrame(columns)
    output_name = f'data/{char_name}.xlsx'
    df.to_excel(output_name, index=False)
