from tekken8_scraper.jun_kazama_scraper import JunKazamaScraper
from tekken8_scraper.migrate_to_sqlite import migrate_to_sqlite

jks = JunKazamaScraper()
jun_data = jks.start_jun_scraper()
sqlite_db = 'jun_kazama.db'
migrate_to_sqlite(jun_data, sqlite_db)