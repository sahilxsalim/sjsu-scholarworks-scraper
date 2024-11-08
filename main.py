#!/usr/bin/env python3
"""
Main entry point for the ScholarWorks Scraper
"""

import logging
from src.scraper import ScholarWorksScraper

def main():
    """Main entry point"""
    try:
        scraper = ScholarWorksScraper()
        scraper.create_projects_csv()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == '__main__':
    main()
