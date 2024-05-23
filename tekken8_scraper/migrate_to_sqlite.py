import sqlite3
from sqlite3 import OperationalError

import pandas as pd
from loguru import logger


def migrate_to_sqlite(frame_data: pd.DataFrame, sqlite_database: str) -> None:
    """
    Migrate data from the dictionary that contains the scraped data to the sqlite database.
    :param frame_data: Pandas DataFrame that contains the scraped data.
    :param sqlite_database: Sqlite database to be created.
    :return: None
    """
    with sqlite3.connect(sqlite_database) as conn:
        query = '''
        CREATE TABLE IF NOT EXISTS JunKazamaData (
            Command TEXT PRIMARY KEY,
            [Hit Level] TEXT,
            Damage TEXT,
            [Start Up Frame] TEXT,
            [Block Frame] TEXT,
            [Hit Frame] TEXT,
            [Counter Hit Frame] TEXT,
            Notes TEXT
        );
        '''
        conn.execute(query)

        logger.info('Truncate JunKazamaData table')
        conn.execute("DELETE FROM JunKazamaData")


    try:
        frame_data.to_sql('JunKazamaData', con=conn, if_exists='append', index=False)
    except OperationalError as e:
        logger.error(e)
        logger.error('Failed to migrate data to SQLite')
    else:
        logger.info('Migrated data to SQLite successfully')


if __name__ == '__main__':
    pass
