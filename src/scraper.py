#!/usr/bin/env python3
"""
ScholarWorks Scraper - A tool to scrape CS project details from SJSU ScholarWorks
"""

import logging
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
from .utils import (
    setup_logging,
    extract_title,
    extract_author,
    extract_advisors,
    extract_keywords,
    extract_publication_date
)

setup_logging()

class ScholarWorksScraper:
    """Scraper for SJSU ScholarWorks CS projects"""
    
    BASE_URL = "https://scholarworks.sjsu.edu"
    
    def __init__(self, output_file: str = 'data/cs_projects.csv'):
        self.output_file = output_file
        
    def get_scholarworks_pages(self) -> List[str]:
        """Get all paginated URLs for the projects listing"""
        response = requests.get(f'{self.BASE_URL}/etd_projects/index_jumplist.json')
        data = response.json()

        # Extract index numbers and find the maximum
        max_index = 0
        base_urls = set()
        
        for item in data:
            url = item['url'].split('#')[0]  # Remove year anchor
            base_urls.add(url)
            
            # Extract index number if present
            if '.html' in url:
                try:
                    index_str = url.split('index.')[-1].split('.html')[0]
                    if index_str.isdigit():
                        max_index = max(max_index, int(index_str))
                except Exception:
                    continue

        return [
            f"{self.BASE_URL}/etd_projects/index.html",
            *[f"{self.BASE_URL}/etd_projects/index.{i}.html" for i in range(2, max_index + 1)]
        ]

    def get_project_links(self) -> List[Dict[str, str]]:
        """Get all project links from the paginated pages"""
        all_projects = []
        pages = self.get_scholarworks_pages()
        
        for page_url in pages:
            logging.info(f"Scraping: {page_url}")
            response = requests.get(page_url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for a_tag in soup.find_all('a', href=True):
                    if "/etd_projects/" in a_tag['href']:
                        try:
                            link_parts = a_tag['href'].split('/')
                            if link_parts[-1].isdigit():
                                all_projects.append({
                                    'title': a_tag.text.strip(),
                                    'url': a_tag['href']
                                })
                        except Exception:
                            continue
        
        logging.info(f"Found {len(all_projects)} total projects")
        return all_projects

    def get_project_details(self, url: str) -> Dict:
        """Scrape detailed information from a project page"""
        full_url = urljoin(self.BASE_URL, url)
        response = requests.get(full_url)
        
        details = {
            'Project Title': 'NA',
            'URL': full_url,
            'Author': 'NA',
            'First Advisor': 'NA',
            'Second Advisor': 'NA',
            'Third Advisor': 'NA',
            'Keywords': 'NA',
            'Publication Date': 'NA',
            'Year': 'NA'
        }
        
        if response.status_code != 200:
            return details

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if it's a Computer Science project
        dept_div = soup.find('div', id='department')
        if not dept_div or 'Computer Science' not in dept_div.text:
            return None
            
        # Extract project details using utility functions
        extract_title(soup, details)
        extract_author(soup, details)
        extract_advisors(soup, details)
        extract_keywords(soup, details)
        extract_publication_date(soup, details)
            
        return details

    def create_projects_csv(self) -> None:
        """Create CSV file with project details"""
        projects = self.get_project_links()
        fieldnames = [
            'Project Title', 'URL', 'Author', 'First Advisor', 
            'Second Advisor', 'Third Advisor', 'Keywords', 
            'Publication Date', 'Year'
        ]
        
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for idx, project in enumerate(projects, 1):
                logging.info(f"Processing project {idx}/{len(projects)}: {project['title']}")
                details = self.get_project_details(project['url'])
                if details:  # Only write if it's a CS project
                    writer.writerow(details)
        
        logging.info(f"\nCSV file '{self.output_file}' has been created!")

def main():
    """Main entry point"""
    scraper = ScholarWorksScraper()
    scraper.create_projects_csv()

if __name__ == '__main__':
    main() 