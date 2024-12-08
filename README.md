# Cricket_Visualization
# Project Description
This project involves fetching cricket statistics for batters and bowlers across different formats (Test, ODI, and T20I) using Selenium. The scraped data is stored in MongoDB for further analysis. Additionally, this data can be visualized and analyzed using tools such as Power BI, Tableau, and other analytical platforms to evaluate player performance trends and insights.

**Source Link:**

https://www.espncricinfo.com/

# Features
**Data Extraction:** Use Selenium to scrape cricket statistics from ESPNcricinfo for any cricketer.

**Data Storage:** Store the scraped data in MongoDB collections organized by player and format.

**Data Analysis:** 

- Perform data analysis and visualizations using analytical tools like Power BI and Tableau.

- Compare player performances, analyze trends, and generate insights.

**Data Scalability:** Extendable to fetch data for any cricketer in any format.

# Data Structure

## Batter Data Fields:

**Teams:** The teams the batter has played against.

**Span:** The career span of the batter in the format.

**Matches:** Number of matches played.

**Innings:** Number of innings played.

**NotOuts:** Times the batter remained not out.

**Runs:** Total runs scored.

**HighestScore:** Highest score in a single inning.

**Average:** Batting average.

**StrikeRate:** Batting strike rate.

**100s:** Number of centuries.

**50s:** Number of half-centuries.


## Bowler Data Fields:

**Teams:** The teams the bowler has bowled against.

**Span:** The career span of the bowler in the format.

**Matches:** Number of matches played.

**Innings:** Number of innings bowled.

**Wickets:** Total wickets taken.

**Average:** Bowling average.

**Economy:** Economy rate.

**StrikeRate:** Bowling strike rate.

## MongoDB Structure:

**Database Name:** player_name_data

**Collection Names:**

- player_name_odi

- player_name_t20

- player_name_test

(Replace player_name with the cricketer's name, e.g., virat_odi, bumrah_t20)

# Installation

**Prerequisites**

- Python 3.7+

- Selenium

- MongoDB

- Power BI or Tableau (Optional, for analysis)

# Future Scope

- Automate data updates using scheduled scripts.

- Expand support for additional cricket statistics like fielding records.

- Integrate with advanced machine learning models for performance prediction.

- Develop an interactive web dashboard for data visualization.

# Contributing
Contributions are welcome!

## Team Members

**Ayushi:** Responsible for fetching bowler data.

**Avinash:** Responsible for fetching batter data.

