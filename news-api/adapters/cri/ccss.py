# https://www.ccss.sa.cr/noticias

import requests
from bs4 import BeautifulSoup

ADAPTER = "Caja Costarricense De Seguro Social"
CODE = 'CCSS'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.ccss.sa.cr/'
DOMAIN = 'https://www.ccss.sa.cr'

def extract_slug(url):
    base_pattern = "noticia?v="
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    parts = date_str.strip().split('/')

    if len(parts) != 3:
        return date_str

    day = parts[0]
    month = parts[1]
    year = parts[2]

    months_spanish = {
        "01": "Ene", "02": "Feb", "03": "Mar", "04": "Abr", "05": "May", "06": "Jun",
        "07": "Jul", "08": "Ago", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dic"
    }
    
    month_short = months_spanish.get(month.zfill(2), month)
    
    return f"{day}/{month_short}/{year}"


def get_headlines():

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('div', class_='mt-3')

        items_data = []

        if container:
            rows = container.find_all('article')

            print(len(rows))

            for row in rows:

                link = row.find('a')
                title = link.text.strip() if link else ''
                # href = link['href'] if link else ''
                date_span = row.find('span', class_='text-muted')
                date = date_span.text.strip() if date_span else ""
                summary = ''
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
    
# TODO: Refactor
def get_news(slug):
    url  = '' + slug
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')        
        
        container = soup.find(class_="wrapper-noticia")