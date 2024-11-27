import requests
import xml.etree.ElementTree as ET
import re
from bs4 import BeautifulSoup

ADAPTER = "Contraloria General de la Republica"
CODE = 'CGR'
LANGUAGE = 'SPA'
COUNTRY = 'CRI'
BASE_URL = 'https://www.cgr.go.cr/10-varios/rss/noticias_rss.xml'


def remove_first_p_tag(description):
    soup = BeautifulSoup(description, "html.parser")
    first_p = soup.find('p')
    if first_p:
        first_p.decompose()

    clean_text = str(soup)
    
    if clean_text.startswith('\n'):
        clean_text = clean_text[1:]

    return clean_text

def extract_first_img_src(description):
    match = re.search(r'<img[^>]+src="([^"]+)"', description)
    return match.group(1) if match else None

def format_date(date_str):    
    parts = date_str.split()    
    
    day = parts[1]
    month = parts[2]
    year = parts[3]    
    
    months_spanish = {
        "Jan": "Ene", "Feb": "Feb", "Mar": "Mar", "Apr": "Abr", "May": "May", "Jun": "Jun",
        "Jul": "Jul", "Aug": "Ago", "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dec": "Dic"
    }    
    
    month_spanish = months_spanish.get(month, month)    
    
    return f"{day}/{month_spanish}/{year}"


def get_text_with_bold(element):
    content = []
    for part in element.descendants:
        if part.name == 'b':
            content.append({'insert': part.text, 'attributes': {'bold': True}})
        elif part.name is None:
            content.append({'insert': part})
    return content

def get_text(element):
    return element.get_text(separator=" ").strip()

def get_headlines():    
    response = requests.get(BASE_URL)
    root = ET.fromstring(response.content)

    items_data = []
    for item in root.findall('.//item'):
        id = item.find('guid').text
        title = item.find('title').text
        body = item.find('description').text
        date_obj = format_date(item.find('pubDate').text)
                
        img_src = extract_first_img_src(body)
        clean_body = remove_first_p_tag(body)        
        

        items_data.append({
            'id': id,
            'title': title,
            'date': date_obj,
            'summary': '', 
            'body': clean_body,
            'slug': '',
            'cover': img_src
        })

    return {"headlines": items_data,"code": CODE, "country": COUNTRY, "language": LANGUAGE}



def get_content(id):    
    content = []
    delta = []
    try:        
        response = requests.get(BASE_URL)
        root = ET.fromstring(response.content)            
        for item in root.findall('.//item'):
            guid = item.find('guid')
            if guid is not None and guid.text == id:                
                title = item.find('title').text
                body = item.find('description').text
                if body is not None:
                    break

        clean_body = remove_first_p_tag(body)        

        soup = BeautifulSoup(clean_body, 'html.parser')

        for tag in soup.find_all(['p', 'ul', 'li', 'a', 'hr']):
            if tag.name == 'p':
                delta.append({'type': 'p', 'text': get_text(tag)})
            elif tag.name == 'ul':
                for li in tag.find_all('li'):
                    delta.append({'type': 'p', 'text': get_text(li)})
            elif tag.name == 'a':
                delta.append({'type': 'p', 'text': get_text(tag)})
            elif tag.name == 'hr':
                delta.append({'type': 'p', 'text': '---'})
        

        return {
            "title": title,
            "content": delta
        }
    except Exception as e:        
        content.append({
            'type': 'p',
            'text': 'Módulo en mantenimiento'
        })
        return {
            "title": "",
            "content": content
        }