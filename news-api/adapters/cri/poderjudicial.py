# https://ministeriopublico.poder-judicial.go.cr/index.php/noticiasjudiciales/noticias-judiciales-2024

import requests
from bs4 import BeautifulSoup
# from helpers.helpers import set_locale
from datetime import datetime

current_year = datetime.now().strftime("%Y");

ADAPTER = "Poder Judicial"
CODE = 'PJ'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = f"https://ministeriopublico.poder-judicial.go.cr/index.php/noticiasjudiciales/noticias-judiciales-{current_year}/"
DOMAIN = 'https://ministeriopublico.poder-judicial.go.cr'

def extract_slug(url):
    base_pattern = "/index.php/noticiasjudiciales/noticias-judiciales-2024/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Eliminar la coma del año, si existe
    date_str = date_str.replace(',', '')
    
    parts = date_str.split()
    
    if len(parts) != 3:
        return date_str
    
    day = parts[0]
    month = parts[1]
    year = parts[2]

    months_spanish = {
        "enero": "Ene", "febrero": "Feb", "marzo": "Mar", "abril": "Abr", "mayo": "May", "junio": "Jun",
        "julio": "Jul", "agosto": "Ago", "septiembre": "Sep", "octubre": "Oct", "noviembre": "Nov", "diciembre": "Dic"
    }
    
    month_short = months_spanish.get(month.lower(), month)

    return f"{day}/{month_short}/{year}"



def get_headlines():   

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('tbody')
        
        items_data = []
        if container:
            rows = container.find_all('tr')
            
            for row in rows:

                link = row.find('a')
                title = link.text.strip() if link else ''
                # href = link['href'] if link else ''
                date = row.find(class_="list-date").text.strip() if row.find(class_="list-date") else ""
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
            return {"error": "Error loading news from this adapter"}
    else:
        return {"error": "Error loading news from this adapter"}
    
def get_content(slug):
    try:
        url = DOMAIN + "/index.php/noticiasjudiciales/noticias-judiciales-2024/" + slug
        print(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            header = soup.find('div', class_='article-header')
            h2 = header.find('h2')
            
            # BODY
            body = soup.find('div', attrs={'itemprop': 'articleBody'})

            content = []
            
            for tag in body.find_all('p'):
                content.append({
                    'type': tag.name,
                    'text': tag.get_text().strip()
                })
            

            return {
                "title": h2.get_text(strip=True),
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