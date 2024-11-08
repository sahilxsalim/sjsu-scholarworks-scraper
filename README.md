# ScholarWorks Scraper

A Python tool to scrape Computer Science project details from SJSU ScholarWorks.

## Features
- Scrapes all CS project details from SJSU ScholarWorks
- Extracts project title, author, advisors, keywords, and publication dates
- Saves data to CSV format

## Prerequisites
- Python 3.x
- pip (Python package installer)

## Installation

1. Clone the repository:
git clone https://github.com/yourusername/scholarworks-scraper.git
cd scholarworks-scraper

2. Install required dependencies:
pip install -r requirements.txt

## Required Dependencies
- beautifulsoup4 (>= 4.12.0) - For HTML parsing
- requests (>= 2.31.0) - For making HTTP requests

## Usage

Run the scraper:
python src/scraper.py

The scraped data will be saved to a CSV file in the output directory.

## Output Format
The scraper generates a CSV file containing the following information for each project:
- Title
- Author
- Advisor(s)
- Keywords
- Publication Date

## Data Analysis
The generated CSV file can be easily imported into Google Sheets for advanced filtering and analysis:

1. Open [Google Sheets](https://sheets.google.com)
2. File > Import > Upload > Select the CSV file
3. Once imported, you can:
   - Use filters (Data > Create a filter) to sort and filter by any column
   - Create pivot tables for statistical analysis
   - Generate visualizations and charts
   - Share and collaborate on the data with others

## Disclaimer
This tool is intended for academic research purposes only.