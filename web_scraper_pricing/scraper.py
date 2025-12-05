"""
Web Scraper for E-commerce Pricing Data
Project: Freelance Data Collection (2019-2021)
Purpose: Automated market pricing benchmarking for SME clients

This script scrapes product prices from public e-commerce sites
and saves them to CSV for competitive analysis.
"""

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# Configuration
OUTPUT_FILE = "pricing_data.csv"
FAKE_URL = "https://realpython.github.io/fake-jobs/"  # Safe demo URL for GitHub

def scrape_pricing_data(url):
    """
    Fetch and parse pricing data from target URL.
    
    Args:
        url (str): Target website URL
        
    Returns:
        list: List of dictionaries containing scraped data
    """
    try:
        # Send HTTP request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        print(f"✓ Successfully fetched data from {url}")
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract data (example: job listings as proxy for product data)
        data_list = []
        items = soup.find_all("div", class_="card-content")
        
        for item in items:
            try:
                title = item.find("h2").text.strip() if item.find("h2") else "N/A"
                company = item.find("h3").text.strip() if item.find("h3") else "N/A"
                location = item.find("p").text.strip() if item.find("p") else "N/A"
                
                data_list.append({
                    "title": title,
                    "company": company,
                    "location": location,
                    "scraped_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            except Exception as e:
                print(f"⚠ Error parsing item: {e}")
                continue
        
        print(f"✓ Scraped {len(data_list)} records")
        return data_list
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching URL: {e}")
        return []

def clean_data(data_list):
    """
    Data cleaning: Remove duplicates, standardize formatting.
    
    Args:
        data_list (list): Raw scraped data
        
    Returns:
        list: Cleaned data
    """
    # Remove duplicates
    unique_data = []
    seen = set()
    
    for record in data_list:
        key = (record['title'], record['company'])
        if key not in seen:
            seen.add(key)
            unique_data.append(record)
    
    print(f"✓ Removed duplicates: {len(data_list)} → {len(unique_data)} records")
    return unique_data

def save_to_csv(data_list, filename=OUTPUT_FILE):
    """
    Export cleaned data to CSV.
    
    Args:
        data_list (list): Cleaned data
        filename (str): Output filename
    """
    if not data_list:
        print("✗ No data to save")
        return
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(data_list)
        
        print(f"✓ Data saved to {filename} ({len(data_list)} rows)")
    
    except Exception as e:
        print(f"✗ Error saving to CSV: {e}")

def main():
    """Main execution pipeline."""
    print("=" * 60)
    print("AUTOMATED PRICING DATA SCRAPER")
    print("=" * 60)
    
    # Step 1: Scrape
    print("\n[Step 1] Scraping data...")
    raw_data = scrape_pricing_data(FAKE_URL)
    
    if not raw_data:
        print("No data scraped. Exiting.")
        return
    
    # Step 2: Clean
    print("\n[Step 2] Cleaning data...")
    cleaned_data = clean_data(raw_data)
    
    # Step 3: Save
    print("\n[Step 3] Saving to CSV...")
    save_to_csv(cleaned_data)
    
    print("\n" + "=" * 60)
    print("✓ Pipeline completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    main()
