# -*- coding: utf-8 -*-
"""webScarping.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vqNHKs5iUfPzFdOPj2Bj2jb7pgo_VT2c
"""

pip install requests beautifulsoup4 pandas

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_artwork_details(artwork_url):
    response = requests.get(artwork_url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {artwork_url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Adjust these selectors based on the detailed page's HTML structure
    painting_name = soup.find('em.object-title').text
    artist_name = soup.find('a.object-artist').text
    image_description = soup.find('p.drawer-content').text
    provenance = soup.find('your_selector_for_provenance').text
    exhibition_history = soup.find('your_selector_for_exhibition_history').text
    image_url = soup.find('your_selector_for_image_url')['src']

    return {
        'Painting Name': painting_name,
        'Artist Name': artist_name,
        'Image Description': image_description,
        'Provenance': provenance,
        'Exhibition History': exhibition_history,
        'Image URL': image_url
    }

def scrape_main_page(main_url):
    response = requests.get(main_url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {main_url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    artwork_links = []
    print("test3")
    # Replace 'your_selector_for_artwork_links' with the correct selector
    hello = soup.find_all('a')
    print(hello)
    # for link in hello:
    #     print("test4")
    #     lk= link.get('href')
    #     print(lk)
    #     artwork_links.append(lk)

    return artwork_links

def main():
    base_url = "https://www.nga.gov/collection-search-result.html?sortOrder=DEFAULT&artobj_downloadable=Image_download_available&pageNumber="
    all_data = []

    total_pages= 2
    page=1
    # Adjust total_pages based on the actual number of pages
    main_url = f"{base_url}{page}"
    artwork_links = scrape_main_page(main_url)
    for artwork_url in artwork_links:
        print("test2")
        artwork_data = scrape_artwork_details(artwork_url)
        if artwork_data:
            all_data.append(artwork_data)
    # for page in range(1, total_pages + 1):
    #     main_url = f"{base_url}{page}"
    #     artwork_links = scrape_main_page(main_url)
    #     print("test")


        # for artwork_url in artwork_links:
        #     print("test2")
        #     artwork_data = scrape_artwork_details(artwork_url)
        #     if artwork_data:
        #         all_data.append(artwork_data)


    # Create a DataFrame and save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv('nga_gallery_data.csv', index=False)

if __name__ == "__main__":
    main()