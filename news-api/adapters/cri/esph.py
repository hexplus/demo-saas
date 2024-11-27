# https://www.esph-sa.com/noticias

import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

# from helpers.helpers import set_locale

ADAPTER = "Empresa de Servicios Públicos de Heredia"
CODE = 'ESPH'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.esph-sa.com/noticias'
DOMAIN = 'https://www.esph-sa.com'

def extract_slug(url):
    base_pattern = "/noticias/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Limpiamos los espacios y dividimos el texto
    parts = date_str.strip().split()
    
    # Verificamos que el formato sea "día de mes del año"
    if len(parts) != 5 or parts[1] != 'de' or parts[3] != 'del':
        return date_str  # Retorna la fecha original si no coincide el formato esperado

    day = parts[0]
    month_name = parts[2]
    year = parts[4]

    # Diccionario para mapear meses en español
    months_spanish = {
        "Enero": "Ene", "Febrero": "Feb", "Marzo": "Mar", "Abril": "Abr", "Mayo": "May", "Junio": "Jun",
        "Julio": "Jul", "Agosto": "Ago", "Septiembre": "Sep", "Octubre": "Oct", "Noviembre": "Nov", "Diciembre": "Dic"
    }

    # Convertimos el nombre del mes al formato abreviado
    month_short = months_spanish.get(month_name, month_name)
    
    return f"{day}/{month_short}/{year}"

def get_headlines():

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('div', class_="grid views-view-grid row")

        items_data = []

        if container:
            rows = container.find_all('div', class_="block-news__item-content col-12 col-sm-6 col-lg-4")

            for row in rows:

                link = row.find('a')
                title = row.find('h2')
                href = link['href'] if link else ''
                date = row.find("time", class_="datetime")

                if date is not None:
                    date_str = date.text
                    print(date_str)
                else:
                    date_str = "Fecha no disponible"
                    print("Elemento <time> con clase 'datetime' no encontrado.")

                summary = ''
                body = ''
                cover = ''
                slug = extract_slug(href)

                items_data.append({
                    'id': '',
                    'title': title,
                    'date': format_date(date_str),
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