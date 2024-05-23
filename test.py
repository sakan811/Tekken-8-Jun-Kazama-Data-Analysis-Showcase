import re
import sqlite3

import pytest

from tekken8_scraper.jun_kazama_scraper import JunKazamaScraper
from tekken8_scraper.migrate_to_sqlite import migrate_to_sqlite
from tekken8_scraper.transform_data import clean_data


def test_clean_numbers():
    input_str = '+14g~+15g'
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == 14
    assert numbers[1] == 15
    assert sum(numbers) == 29
    assert sum(numbers) / len(numbers) == 14.5

    input_str = '-6 (high blocked)'
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == -6

    input_str = "+21a~+64a (-5~+38)"
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == 21
    assert numbers[1] == 64
    assert numbers[2] == -5
    assert numbers[3] == 38
    assert sum(numbers) == 118
    assert sum(numbers) / len(numbers) == 29.5

    input_str = ",i27~28"
    # Extract numeric values using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert sum(numbers) == 55
    assert sum(numbers) / len(numbers) == 27.5

    input_str = "7,9,12,21"
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert sum(numbers) == 49
    assert sum(numbers) / len(numbers) == 12.25

    input_str = "-6~+37g"
    # Extract numbers using regular expressions
    numbers = re.findall(r'-?\d+', input_str)
    # Convert numbers to integers
    numbers = [int(num) for num in numbers]
    assert numbers[0] == -6
    assert numbers[1] == 37
    assert sum(numbers) == 31

    input_str = "-6~+37g"
    match = re.search(r'-?\d+', input_str)

    if match:
        # Convert the first found number to an integer
        number = int(match.group(0))
        assert number == -6


def test_full_process():
    jks = JunKazamaScraper()
    jun_data = jks.start_jun_scraper()
    jun_data_cleaned = clean_data(jun_data)
    sqlite_db = 'jun_kazama_test.db'
    migrate_to_sqlite(jun_data_cleaned, sqlite_db)

    with sqlite3.connect(sqlite_db) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM JunKazamaData')
        data = cursor.fetchall()
        assert len(data) > 0


if __name__ == '__main__':
    pytest.main([__file__])
