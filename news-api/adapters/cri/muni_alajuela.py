# https://www.munialajuela.go.cr/News/Index

import requests
from bs4 import BeautifulSoup

ADAPTER = "Municipalidad Alajuela"
CODE = 'MPAJ'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = "https://www.munialajuela.go.cr/News/Index"
DOMAIN = 'https://www.munialajuela.go.cr/'

def extract_slug(url):
    base_pattern = "/News/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url

def format_date(date_str):
    # Eliminar cualquier punto (.) en el mes
    date_str = date_str.replace('.', '')

    # Dividir la fecha en partes (día, mes, año)
    parts = date_str.split()
    
    if len(parts) != 3:
        return date_str  # Si la fecha no tiene el formato correcto, la retorna como está
    
    day = parts[0]
    month = parts[1]
    year = parts[2]

    # Revisar si el año tiene 4 dígitos
    if len(year) != 4 or not year.isdigit():
        return "Formato de fecha incorrecto"

    # Diccionario de meses abreviados en español
    months_spanish = {
        "enero": "Ene", "febrero": "Feb", "marzo": "Mar", "abril": "Abr", "mayo": "May", "junio": "Jun",
        "julio": "Jul", "agosto": "Ago", "septiembre": "Sep", "octubre": "Oct", "noviembre": "Nov", "diciembre": "Dic",
        "ene": "Ene", "feb": "Feb", "mar": "Mar", "abr": "Abr", "may": "May", "jun": "Jun", 
        "jul": "Jul", "ago": "Ago", "sep": "Sep", "oct": "Oct", "nov": "Nov", "dic": "Dic"
    }
    
    # Obtener la abreviatura del mes
    month_short = months_spanish.get(month.lower(), month)

    # Retornar la fecha en el formato solicitado: 19/Sep/2024
    return f"{day}/{month_short}/{year}"

def get_headlines():

    response = requests.get(BASE_URL)
    
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        container = soup.find('div', class_="column_container")
        

        items_data = []
        if container:
            rows = container.find_all('div')
            
            for row in rows:

                link = row.find('a')
                title = row.find(class_="bolder pad_t_1 pad_b_3 block fs_11_1024_st").text
                # href = link['href'] if link else ''
                date = row.find(class_="inline pad_05 fs_08 bolder uppercase bck_white").text.strip() if row.find(class_="inline pad_05 fs_08 bolder uppercase bck_white") else ""
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
    

# TODO: Refactor
def get_news(slug):
    url  = '' + slug
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')        
        
        container = soup.find(class_="wrapper-noticia")