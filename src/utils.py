import logging
from typing import Dict
from bs4 import BeautifulSoup

def setup_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def extract_title(soup: BeautifulSoup, details: Dict) -> None:
    """Extract project title"""
    title_div = soup.find('div', id='title')
    if title_div and title_div.h1:
        details['Project Title'] = title_div.h1.text.strip()

def extract_author(soup: BeautifulSoup, details: Dict) -> None:
    """Extract author name"""
    author_p = soup.find('p', class_='author')
    if author_p and author_p.strong:
        details['Author'] = author_p.strong.text.strip()

def extract_advisors(soup: BeautifulSoup, details: Dict) -> None:
    """Extract advisor information"""
    advisor_divs = {
        'advisor1': 'First Advisor',
        'advisor2': 'Second Advisor',
        'advisor3': 'Third Advisor'
    }
    
    for div_id, detail_key in advisor_divs.items():
        advisor_div = soup.find('div', id=div_id)
        if advisor_div and advisor_div.find('p'):
            details[detail_key] = advisor_div.find('p').text.strip()

def extract_keywords(soup: BeautifulSoup, details: Dict) -> None:
    """Extract project keywords"""
    keywords_div = soup.find('div', id='keywords')
    if keywords_div and keywords_div.find('p'):
        details['Keywords'] = keywords_div.find('p').text.strip()

def extract_publication_date(soup: BeautifulSoup, details: Dict) -> None:
    """Extract publication date and year"""
    pub_date_div = soup.find('div', id='publication_date')
    if pub_date_div and pub_date_div.find('p'):
        pub_date = pub_date_div.find('p').text.strip()
        details['Publication Date'] = pub_date
        
        try:
            year = pub_date.split()[-1]
            if year.isdigit():
                details['Year'] = year
        except Exception:
            pass
