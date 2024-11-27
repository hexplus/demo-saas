# https://www.earth.ac.cr/historias-earth/

import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
# from helpers.helpers import set_locale

ADAPTER = "Universidad Earth"
CODE = 'EARTH'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.earth.ac.cr/historias-earth/'
DOMAIN = 'https://www.earth.ac.cr'

def extract_slug(url):
    base_pattern = "https://www.earth.ac.cr/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    parts = date_str.strip().split('/')

    if len(parts) == 2:
        month = parts[0]
        year = parts[1]
    elif len(parts) == 3:
        day = parts[0]
        month = parts[1]
        year = parts[2]
    else:
        return date_str

    months_spanish = {
        "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr", "05": "May", "06": "Jun",
        "07": "Jul", "08": "Ago", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
    }
    
    month_short = months_spanish.get(month.zfill(2), month)
    
    if len(parts) == 2:
        return f"{month_short}/{year}"
    else:
        return f"{day}/{month_short}/{year}"



def get_headlines():

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find(class_='elementor-posts-container')

        items_data = []

        if container:
            rows = container.find_all('article')

            for row in rows:

                link = row.find('a')
                title = row.find("h3").text
                # href = link['href'] if link else ''
                date = row.find(class_="elementor-post__meta-data").text.strip()
                summary = row.find(class_="elementor-post__excerpt").text.strip()
                body = ''
                cover = ''
                slug = extract_slug(link['href'])

                items_data.append({
                    'id': '',
                    'title': title,
                    'date': format_date(date),
                    'summary': summary, 
                    'body': body,
                    'slug':  slug,
                    'cover': cover
                })

            return {"headlines": items_data,"code": CODE, "country": COUNTRY, "language": LANGUAGE}
        else:
            return {"error": "Error loading news from this adapter."}
    else:
        return {"error": "Error loading news from this adapter"}
    
def get_content(slug):
    try:
        url = DOMAIN + "/" + slug
        print(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            h1 = soup.find('h1', class_="elementor-heading-title")
            print(h1)

            # BODY
            body = soup.find('div', attrs={'data-elementor-type': 'wp-post'})

            content = []
            
            for tag in body.find_all(['p']):
                content.append({
                    'type': tag.name,
                    'text': tag.get_text().strip()
                })

            return {
                "title": h1.get_text(strip=True),
                "content": content
            }
        else:
            print("Unable to load URL")
    except Exception as e:
        content.append({
            'type': 'p',
            'text': 'Módulo en mantenimiento'
        })
        return {
            "title": "",
            "content": content
        }