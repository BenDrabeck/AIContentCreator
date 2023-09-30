import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def read_video_ids():
    try:
        df = pd.read_csv('cached.csv')
        return df['ID'].tolist()
    except FileNotFoundError:
        print("Oi, cached.csv not found!")
        return []

def scrape_tiktok(video_ids):
    scraped_data = []
    for video_id in video_ids:
        # TODO: Your web scraping code here
        genre = ''  # Scrape this
        views = ''  # Scrape this
        likes = ''  # Scrape this
        shares = ''  # Scrape this
        comments = ''  # Scrape this
        time_posted = ''  # Scrape this
        scraped_data.append([video_id, genre, views, likes, shares, comments, time_posted])
    return scraped_data

def save_to_csv(data):
    header = ['video_id', 'genre', 'views', 'likes', 'shares', 'comments', 'time_posted']
    with open('tiktok_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__ == "__main__":
    video_ids = read_video_ids()
    scraped_data = scrape_tiktok(video_ids)
    save_to_csv(scraped_data)
