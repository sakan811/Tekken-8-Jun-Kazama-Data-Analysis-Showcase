import bs4
import requests
from bs4 import BeautifulSoup
from loguru import logger

logger.add('../tekken_8.log',
           format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {name} | {module} | {function} | {line} | {message}",
           mode='w')


class JunKazamaScraper:
    def __init__(self):
        logger.info("JunKazamaScraper initialized")

    def _web_scrape(self, html_content: str) -> dict[str, list]:
        """
        Web-scrape HTML content.
        :param html_content: HTML as String.
        :return: Dictionary containing all scraped data.
        """
        logger.info('Starting Web-scraping process...')

        soup = BeautifulSoup(html_content, 'html.parser')
        tbody_content = soup.find('tbody')

        td_contents = tbody_content.find_all('td')

        frame_data_dictionary = self._append_data_to_dict(td_contents)

        return frame_data_dictionary

    @staticmethod
    def _append_data_to_dict(td_contents: bs4.ResultSet) -> dict[str, list]:
        """
        Append bs4 ResultSet data to dictionary.
        :param td_contents: Bs4 ResultSet of the target data.
        :return: Dictionary containing all scraped data.
        """
        logger.info('Appending data to dictionary...')

        frame_data_dict = {
            "Command": [],
            "Hit Level": [],
            "Damage": [],
            "Start Up Frame": [],
            "Block Frame": [],
            "Hit Frame": [],
            "Counter Hit Frame": [],
            "Notes": []
        }

        num_columns = len(frame_data_dict)
        for i, td_content in enumerate(td_contents):
            if i % num_columns == 0:
                frame_data_dict["Command"].append(td_content.text)
            elif i % num_columns == 1:
                frame_data_dict["Hit Level"].append(td_content.text)
            elif i % num_columns == 2:
                frame_data_dict["Damage"].append(td_content.text)
            elif i % num_columns == 3:
                frame_data_dict["Start Up Frame"].append(td_content.text)
            elif i % num_columns == 4:
                frame_data_dict["Block Frame"].append(td_content.text)
            elif i % num_columns == 5:
                frame_data_dict["Hit Frame"].append(td_content.text)
            elif i % num_columns == 6:
                frame_data_dict["Counter Hit Frame"].append(td_content.text)
            elif i % num_columns == 7:
                frame_data_dict["Notes"].append(td_content.text)

        return frame_data_dict

    @staticmethod
    def _get_page_html() -> str:
        """
        Get page's HTML content.
        :return: page's HTML content as String.
        """
        logger.info('Getting Jun Kazama page HTML...')

        url = 'https://rbnorway.org/jun-t8-frames/'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        try:
            logger.info(f'Send GET request to URL: {url}')
            response = requests.get(url, headers=headers)

            # Raise an HTTPError for bad responses (4xx and 5xx)
            response.raise_for_status()

            html_content = response.text
        except requests.RequestException as e:
            logger.error(f'Failed to fetch the page HTML: {e}')
        else:
            logger.info('Successfully fetched the page HTML')
            return html_content

    def start_jun_scraper(self) -> dict[str, list]:
        """
        Start Jun Kazama data scraper.
        :return: Dictionary containing all scraped data.
        """
        logger.info('Starting Jun Kazama scraper...')

        html_content = self._get_page_html()
        return self._web_scrape(html_content)


if __name__ == '__main__':
    pass
