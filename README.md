# Tekken 8 Jun Kazama Data Analysis Showcase
Showcase visualizations of Jun Kazama data in Tekken 8.

## Status
#### 🎉 **Project Completed** 🎉

Latest Project Update: 9 July 2024

[![CodeQL](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/codeql.yml)  
[![Python application](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sakan811/Tekken-8-Jun-Kazama-Data-Analysis-Showcase/actions/workflows/python-app.yml)

## Project Details
Focus primarily on Jun Kazama from Tekken 8.   

Some move variations were excluded.

Jun Kazama data is based on https://rbnorway.org/jun-t8-frames/.

## Visualizations
Visualizations Latest Update: 25 June 2024

[Power BI](https://app.powerbi.com/view?r=eyJrIjoiMjA3OTE4NTctM2UxNC00MjE3LWI4Y2MtYTk0OWMzZDE1NDFiIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D)

[Instagram](https://www.instagram.com/p/C8o3dsavTch/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)  

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid09d1uhSATHBRvcrHqjkNxk6YxGHkeo8NgQEeMhig9KQLsgnF2Ph1bwMRG3PmgfzmPl&id=61553626169836)

## Analysis Details
Frame (Only first hit is considered)

Frame_Advantage_on_Block (Only last action is considered, or if the move is stopped when blocked)

Frame_Advantage_on_Hit (Only last action is considered)

Moves' **Frame** is mostly 13 – 20 frames

Moves' **Damage** is mostly 16 – 37 damages

Moves' **Frame_Advantage_on_Block** is mostly -12 – 0 frames

Moves' **Frame_Advantage_on_Hit** is mostly 2 – 21 frames

Frame and Dmg/Frame have a positive relationship

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

