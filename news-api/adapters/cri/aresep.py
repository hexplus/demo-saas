# https://aresep.go.cr/categoria/noticias/

import requests
from bs4 import BeautifulSoup

ADAPTER = "ARESEP"
CODE = 'ARSP'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = "https://aresep.go.cr/categoria/noticias/"
DOMAIN = 'https://aresep.go.cr/'

def extract_slug(url):
    base_pattern = "https://aresep.go.cr/noticias/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Eliminar las palabras "de" y cualquier coma, pero no otros caracteres
    date_str = date_str.replace(',', '').replace(' de ', ' ')

    # Dividir la fecha en partes
    parts = date_str.split()
    
    if len(parts) != 3:
        return date_str  # Si la fecha no tiene el formato correcto, la retorna como está
    
    day = parts[0]
    month = parts[1]
    year = parts[2]

    # Revisar si el año tiene 4 dígitos
    if len(year) != 4 or not year.isdigit():
        return "Año incorrecto"

    # Diccionario de meses abreviados en español
    months_spanish = {
        "enero": "Ene", "febrero": "Feb", "marzo": "Mar", "abril": "Abr", "mayo": "May", "junio": "Jun",
        "julio": "Jul", "agosto": "Ago", "septiembre": "Sep", "octubre": "Oct", "noviembre": "Nov", "diciembre": "Dic"
    }
    
    # Obtener la abreviatura del mes
    month_short = months_spanish.get(month.lower(), month)

    # Retornar la fecha en el formato solicitado: 21/Ene/2024
    return f"{day}/{month_short}/{year}"


def get_headlines():   

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('ul', class_="list-download")
        
        items_data = []
        if container:
            rows = container.find_all('li')
            
            for row in rows:

                link = row.find('a')
                title = link.text.split(' - ')[0].strip()
                # href = link['href'] if link else ''
                date = row.find(class_="posted-on").text.strip() if row.find(class_="posted-on") else ""
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
        url = DOMAIN + "/noticias/" + slug
        print(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            header = soup.find('header', class_='entry-header')
            h1 = header.find('h1', class_='entry-title') if header else None            

            # BODY
            body = soup.find('div', class_='entry-content')            
                
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