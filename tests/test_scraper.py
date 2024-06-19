import sqlite3

import pytest

from tekken8_scraper.jun_kazama_scraper import JunKazamaScraper
from tekken8_scraper.migrate_to_sqlite import migrate_to_sqlite
from tekken8_scraper.transform_data import clean_data


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
