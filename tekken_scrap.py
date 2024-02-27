import re
import bs4
from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from loguru import logger

# remove default loguru sink
logger.remove()

logger.add('tekken_8.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


def return_match_for_extract_first_digit(text: str) -> re.Match[str]:
    """
    Return Match for extracting first digit from String contain digits with regular expression in between them.
    For example: '-19~-20'
    :param text: The input text string to match against.
    :return: A re.Match object representing the first digit match.
    """
    logger.info('Returning Match for extracting first digit from string...')
    return re.match(r'([+-]?)\d+', text)


def web_scrap(char_url_list: list[str]) -> None:
    """
    Web scrape from URL in URL list.
    :param char_url_list: List containing URLs of each character page.
    :return: None
    """
    logger.info('Web scraping...')
    try:
        for char_url in char_url_list:
            logger.info('Open browser')
            driver = webdriver.Chrome()

            logger.info('Open webpage from URL')
            driver.get(char_url)
            logger.debug(f'{char_url = }')

            logger.info('Get HTML content')
            first_page_content: str = driver.page_source
            logger.debug(f'{first_page_content = }')

            logger.info('Split character name from URL')
            char_name: str = char_url.split("/")[-2]
            logger.debug(f'{char_name = }')

            logger.info('Add first page content to list')
            page_contents = [first_page_content]
            logger.debug(f'{page_contents = }')

            logger.info('Getting HTML from other pages of same character...')
            while True:
                logger.info('Get HTML content of current page')
                current_page_source: str = driver.page_source
                logger.debug(f'{current_page_source = }')

                try:
                    next_page_xpath: str = '//*[@id="tablesome__container"]/nav/ul/li[6]'

                    logger.info(f'Find next page web element by {next_page_xpath = }')
                    next_page_element: WebElement = driver.find_element(By.XPATH, next_page_xpath)

                    logger.info('Click at web element')
                    next_page_element.click()

                    logger.info('Capture the new page source after clicking the button')
                    new_page_source: str = driver.page_source
                    logger.debug(f'{new_page_source = }')

                    logger.info('If the page content has not changed (indicating end of pagination), break the loop')
                    if current_page_source == new_page_source:
                        print("No more dynamically changing pages found. Exiting loop.")
                        logger.warning('No more dynamically changing pages found. Exiting loop.')
                        break

                    logger.info('Append the new page source to the list of page_contents')
                    page_contents.append(new_page_source)
                except NoSuchElementException as e:
                    print("Next button element not found. Exiting loop.")
                    logger.error(f'Error: {e}')
                    break

            logger.info('Close browser')
            driver.quit()

            logger.info('Create columns for storing data')
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
            logger.debug(f'{columns = }')

            logger.info('Scraping HTML elements from all pages of given character...,'
                        'Looping through \'page_contents\' list...')
            for content in page_contents:
                logger.info('Parse HTML of webpage to BeautifulSoup')
                soup = BeautifulSoup(content, 'html.parser')

                tag: str = 'td'
                class_name: str = 'tablesome__cell tablesome__cell--text'
                logger.info(f'Find all desired web elements by {tag = } and {class_name = }')
                elements: bs4.ResultSet = soup.find_all(tag, class_=class_name)
                logger.debug(f'{elements = }')

                logger.info('Inserting extracted data to correspond column using column index...')
                for i, element in enumerate(elements):
                    logger.info('Calculate column index')
                    column_index: int = i % 8
                    logger.debug(f'{column_index = }')

                    element_text: str = element.text
                    logger.debug(f'{element_text = }')

                    if column_index == 0:
                        logger.info(f'{column_index = }, append to Command column')
                        columns['Command'].append(element_text)
                    elif column_index == 1:
                        logger.info(f'{column_index = }, append to Hit level column')
                        columns['Hit level'].append(element_text)
                    elif column_index == 2:
                        logger.info(f'{column_index = }, append to Damage column')
                        if element_text == '-' or element_text == '?':
                            logger.info('Extracted data is - or ?, add None to Damage column')
                            columns['Damage'].append(None)
                        else:
                            logger.info('Extracted data is not - or ?')

                            logger.info('Extract numerical values using regular expression')
                            damage_values: list = re.findall(r'\d+', element_text)
                            logger.debug(f'{damage_values = }')

                            logger.info('Convert the extracted values to integers')
                            damage_integers = [int(value) for value in damage_values]
                            logger.debug(f'{damage_integers = }')

                            logger.info('Add to Damage column')
                            columns['Damage'].append(sum(damage_integers))
                    elif column_index == 3:
                        logger.info(f'{column_index = }, append to Startup column')

                        match: re.Match[str] = return_match_for_extract_first_digit(element_text)
                        logger.debug(f'{match = }')
                        if match:
                            logger.info(f'Extracted data is in \'match\'')

                            logger.info('Use regular expression to extract the first integer')
                            first_int = int(re.search(r'\d+', match.group()).group())
                            logger.debug(f'{first_int = }')

                            logger.info('Add to Startup column')
                            columns['Startup'].append(first_int)
                        elif element_text.isdigit():
                            logger.info('Extracted data consists of 1 digit only, convert it into integer,'
                                        'Add to Startup column.')
                            columns['Startup'].append(int(element_text))
                        else:
                            logger.info('Extracted data have only non-numeric values, add None to Startup column.')
                            columns['Startup'].append(None)
                    elif column_index == 4:
                        logger.info(f'{column_index = }, append to Block column')

                        match: re.Match[str] = return_match_for_extract_first_digit(element_text)
                        logger.debug(f'{match = }')
                        if match:
                            logger.info(f'Extracted data is in \'match\'')

                            logger.info('Extract the sign and integer part')

                            logger.info('Group 1 captures the sign')
                            sign = match.group(1)
                            logger.debug(f'{sign = }')

                            logger.info('Convert the matched digits to an integer')
                            first_int = int(match.group())
                            logger.debug(f'{first_int = }')

                            logger.info('Add to Block column')
                            columns['Block'].append(-first_int)
                        elif element_text.isdigit():
                            logger.info('Extracted data consists of 1 digit only, convert it into integer,'
                                        'Add to Block column.')
                            columns['Block'].append(int(element_text))
                        else:
                            logger.info('Extracted data have only non-numeric values, add None to Block column.')
                            columns['Block'].append(None)
                    elif column_index == 5:
                        logger.info(f'{column_index = }, append to Hit column')

                        match: re.Match[str] = return_match_for_extract_first_digit(element_text)
                        logger.debug(f'{match = }')
                        if match:
                            logger.info(f'Extracted data is in \'match\'')

                            logger.info('Extract the sign and integer part')

                            logger.info('Group 1 captures the sign')
                            sign = match.group(1)
                            logger.debug(f'{sign = }')

                            logger.info('Convert the matched digits to an integer')
                            first_int = int(match.group())
                            logger.debug(f'{first_int = }')

                            logger.info('Add to Hit column')
                            columns['Hit'].append(first_int)
                        elif element_text.isdigit():
                            logger.info('Extracted data consists of 1 digit only, convert it into integer,'
                                        'Add to Block column.')
                            columns['Hit'].append(int(element_text))
                        elif re.match(r'^[a-zA-Z]+$', element_text):
                            logger.info('Extracted data is English word')
                            columns['Hit'].append(70)
                        else:
                            logger.info('Extracted data have only non-numeric values, add None to Hit column.')
                            columns['Hit'].append(None)
                    elif column_index == 6:
                        columns['Counter Hit'].append(element_text)
                    elif column_index == 7:
                        columns['Notes'].append(element_text)

            logger.info('Create DataFrame from \'columns\'')
            df = pd.DataFrame(columns)

            output_name = f'data/{char_name}.xlsx'
            logger.debug(f'{output_name = }')

            logger.info('Save to Excel at \'output_name\'')
            df.to_excel(output_name, index=False)
    except Exception as e:
        logger.error(f'Error: {e}')


def get_main_page_html() -> str:
    """
    Get main page HTML
    :return: HTML of the main page
    """
    logger.info('Getting main page HTML...')
    logger.info('Open browser')
    driver = webdriver.Chrome()

    url = 'https://tekken8framedata.com/'
    logger.debug(f'{url = }')

    logger.info('Open web page from URL')
    driver.get(url)

    main_page_contents: str = driver.page_source

    logger.info('Close browser')
    driver.close()
    return main_page_contents


def find_character_page_url(main_page_contents: str) -> ResultSet:
    """
    Find all character page URLs from the main page HTML.
    :param main_page_contents: main page HTML
    :return: All character URLs as bs4.ResultSet
    """
    logger.info('Finding all character page URLs...')
    logger.info('Parse HTML content to BeautifulSoup')
    soup = BeautifulSoup(main_page_contents, 'html.parser')

    pattern: re.Pattern[str] = re.compile(r'tekken-8-frame-data')
    logger.info(f'Find all {pattern = } by tag \'a\'')
    char_urls: ResultSet = soup.find_all('a', href=pattern)
    return char_urls


def make_character_url_list(char_urls: ResultSet) -> list[str]:
    """
    Make character URLs list.
    :param char_urls: All character URLs as bs4.ResultSet
    :return: character URLs list
    """
    logger.info('Making character URLs list...')
    logger.info('Make list of character URLs')
    char_url_list = [char_url['href'] for char_url in char_urls]
    logger.debug(f'{char_url_list = }')

    logger.info('Convert list into set and back to list to delete duplicate URLs')
    char_url_list = list(set(char_url_list))
    return char_url_list


def main() -> None:
    main_page_contents: str = get_main_page_html()
    logger.debug(f'{main_page_contents = }')

    char_urls: ResultSet = find_character_page_url(main_page_contents)
    logger.debug(f'{char_urls = }')

    char_url_list: list[str] = make_character_url_list(char_urls)
    logger.debug(f'{char_url_list = }')

    web_scrap(char_url_list)


if __name__ == '__main__':
    main()
