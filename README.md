# Tekken 8 Jun Kazama Data Analysis Showcase
Showcase visualizations of Jun Kazama data in Tekken 8.

## Status
#### 🎉 **Project Completed** 🎉

[![CodeQL](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/codeql.yml)  

[![Python application](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/python-app.yml)

## Project Details
Focus primarily on Jun Kazama from Tekken 8.   

Some move variations were excluded.

Jun Kazama data is based on https://rbnorway.org/jun-t8-frames/.

## Visualizations

[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMjA3OTE4NTctM2UxNC00MjE3LWI4Y2MtYTk0OWMzZDE1NDFiIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)

[Instagram](https://www.instagram.com/p/C_IK6JpOQuW/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid0r3uFaCXj9aGmnjHgokiR6X7sQ24tTxL5f67Mhc33xmnVpwSHPg3MFiNvn1zqntB1l&id=61553626169836)

## Disclaimers
Moves with multiple hits had their frame averaged.


## Codebase Details

### To scrape Jun Kazama data
- Go to [main.py](main.py)
- Specify the SQLite database name if needed
    ```
    sqlite_db = 'jun_kazama.db' # can be specified  
  ```
- Run the script

### [tekken8_scraper](tekken8_scraper) Package
[jun_kazama_scraper.py](tekken8_scraper%2Fjun_kazama_scraper.py)
- Scrape Jun Kazama data from https://rbnorway.org/jun-t8-frames/
- Store in Pandas DataFrame

[transform_data.py](tekken8_scraper%2Ftransform_data.py)
- Clean data in the DataFrame

[migrate_to_sqlite.py](tekken8_scraper%2Fmigrate_to_sqlite.py)
- Migrate the DataFrame to SQLite database
  - Create SQLite database named **jun_kazama.db** 
    - Database name can be specified in [main.py](main.py)

