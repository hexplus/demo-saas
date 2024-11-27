# https://noticiassanjose.com/

import requests
from bs4 import BeautifulSoup

ADAPTER = "Municipalidad San José"
CODE = 'MPSJ'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = "https://noticiassanjose.com/"
DOMAIN = 'https://noticiassanjose.com'

def extract_slug(url):
    base_pattern = "https://noticiassanjose.com/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Eliminar solo la coma, pero no otros caracteres
    date_str = date_str.replace(',', '')
    
    parts = date_str.split()
    
    if len(parts) != 3:
        return date_str
    
    day = parts[0]
    month = parts[1]
    year = parts[2]

    # Revisar si el año sigue teniendo los 4 dígitos
    if len(year) != 4 or not year.isdigit():
        return "Año incorrecto"

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
        
        container = soup.find('div', class_="grupo_noticias_b")
        
        items_data = []
        if container:
            rows = container.find_all('article')
            
            for row in rows:

                link = row.find('a')
                title = row.find('h2').text.strip()
                # href = link['href'] if link else ''
                date = row.find(class_="date").text.strip() if row.find(class_="date") else ""
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
        url = DOMAIN + "/" + slug
        print(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            h1 = soup.find('h1', class_="text-transform-none gris display-4")

            # BODY
            body = soup.find('div', class_="page")

            content = []
            
            for tag in body.find_all('p'):
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