# https://www.fecobacr.com/noticia/

import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup
# from helpers.helpers import set_locale

ADAPTER = "Federación Costarricense de Baloncesto"
CODE = 'FECOBA'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.fecobacr.com/noticia/'
DOMAIN = 'https://www.fecobacr.com'

def extract_slug(url):
    base_pattern = "https://www.fecobacr.com/noticia/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Separar la parte de la fecha y eliminar espacios
    date_part = date_str.split("/")[0].strip()
    
    # Limpiamos los espacios y dividimos el texto
    parts = date_part.split()
    
    # Verificamos que el formato sea "día mes año"
    if len(parts) != 3:
        return date_str  # Retorna la fecha original si no coincide el formato esperado

    day = parts[0]
    month_name = parts[1]
    year = parts[2]

    # Diccionario para mapear meses en español
    months_spanish = {
        "Enero": "Ene", "Febrero": "Feb", "Marzo": "Mar", "Abril": "Abr", "Mayo": "May", "Junio": "Jun",
        "Julio": "Jul", "Agosto": "Ago", "Septiembre": "Sep", "Octubre": "Oct", "Noviembre": "Nov", "Diciembre": "Dic"
    }

    # Convertimos el nombre del mes al formato abreviado
    month_short = months_spanish.get(month_name.capitalize(), month_name)

    return f"{day}/{month_short}/{year}"


def get_headlines():

    response = requests.get(BASE_URL)
    
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('div', class_="col-xs-12 col-sm-12 col-md-12 entries")

        items_data = []

        if container:
            rows = container.find_all('div', class_="col-xs-12 col-sm-6 col-md-4 entry clearfix")

            for row in rows:

                link = row.find('a')
                title = row.find(class_="entry-title").text
                date = row.find(class_="entry-meta").text
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
    

def get_content(slug):
    try:
        url = DOMAIN + "/noticia/" + slug
        print(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            header = soup.find('div', class_='entry-title')
            h3 = soup.find('h3') if header else None            

            # BODY
            body = soup.find('div', class_='entry-content')            
                
            content = []
            
            for tag in body.find_all(['p']):
                content.append({
                    'type': tag.name,
                    'text': tag.get_text().strip()
                })

            return {
                "title": h3.get_text(strip=True),
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