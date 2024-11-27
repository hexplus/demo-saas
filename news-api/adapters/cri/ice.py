import requests
from bs4 import BeautifulSoup
# from helpers.helpers import set_locale

ADAPTER = "Instituto Costarricense de Electricidad"
CODE = 'ICE'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.grupoice.com/wps/portal/ICE/quienessomos/sala-prensa/sala-de-prensa/'
DOMAIN = 'https://www.grupoice.com'


def extract_slug(url):    
    base_pattern = "/wps/portal/ICE/quienessomos/sala-prensa/sala-de-prensa/noticias/"
    
    if url.startswith(base_pattern):
        return url[len(base_pattern):]
    else:
        return url
    



def format_date(date_str):    
    parts = date_str.split()    
    
    day = parts[0]
    month = parts[2]
    year = parts[4]    
    
    months_spanish = {
        "enero": "Ene", "febrero": "Feb", "marzo": "Mar", "abril": "Abr", "mayo": "May", "junio": "Jun",
        "julio": "Jul", "agosto": "Ago", "septiembre": "Sep", "octubre": "Oct", "noviembre": "Nov", "diciembre": "Dic"
    }
    
    # Convertir el mes al formato abreviado
    month_short = months_spanish.get(month.lower(), month)
    
    # Formatear la fecha como "11/Oct/2024"
    return f"{day}/{month_short}/{year}"

def get_headlines():   

    response = requests.get(BASE_URL)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')        
        
        container = soup.find(class_="home-sala-prensa")
        
        items_data = []
        if container:            
            rows = container.find_all(class_="noticia")            
            
            for row in rows:                
                title = row.find(class_='titulo-noticia').text
                summary = row.find(class_="descripcion-breve").text
                body = ''
                date = row.find(class_="fecha").text
                link = row.find('a')
                cover = row.find('img')

                slug = extract_slug(link['href'])

                
                items_data.append({
                    'id': '',
                    'title': title,
                    'date': format_date(date),
                    'summary': summary, 
                    'body': body,
                    'slug':  slug,
                    'cover': DOMAIN + cover['src']
                })

            return {"headlines": items_data,"code": CODE, "country": COUNTRY, "language": LANGUAGE}
        else:
            return {"error": "Error loading news from this adapter"}
    else:
        return {"error": "Error loading news from this adapter"}
    



def get_content(slug):
    try:
        formatted_slug = slug.replace(" ", "+")

        url = DOMAIN + "/wps/portal/ICE/quienessomos/sala-prensa/sala-de-prensa/noticias/" + formatted_slug
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            header = soup.find('div', class_='col-sm-12 col-md-12 col-lg-8 offset-lg-2')
            h1 = header.find('h1', class_='title') if header else None

            # BODY
            body = soup.find('div', class_='RTF-Noticia')

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
