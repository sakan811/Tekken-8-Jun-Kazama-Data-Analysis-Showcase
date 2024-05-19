from tekken8_scraper.jun_kazama_scraper import JunKazamaScraper
from tekken8_scraper.migrate_to_sqlite import migrate_to_sqlite
from tekken8_scraper.transform_data import clean_data

jks = JunKazamaScraper()
jun_data = jks.start_jun_scraper()
jun_data_cleaned = clean_data(jun_data)
sqlite_db = 'jun_kazama.db'
migrate_to_sqlite(jun_data_cleaned, sqlite_db)
