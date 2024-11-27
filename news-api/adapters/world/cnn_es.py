import requests
from bs4 import BeautifulSoup
import re

ADAPTER = "CNN en Español"
CODE = 'CNNE'
LANGUAGE = 'SPA'
COUNTRY = 'INT'
DOMAIN = 'https://cnnespanol.cnn.com'
BASE_URL = DOMAIN + '/'

def extract_categories_slug(url):
    if url.startswith(BASE_URL):
        return url[len(BASE_URL):]
    else:
        return url


def edit_img(url):
    new_url = url.replace("720", "270").replace("1280", "480")
    return new_url

def extract_date_in_spanish(slug):
    date_pattern = re.search(r'/(\d{4})/(\d{2})/(\d{2})/', slug)
    
    if date_pattern:        
        year, month, day = date_pattern.groups()
        months_in_spanish = {
            '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
            '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
            '09': 'Set', '10': 'Oct', '11': 'Nov', '12': 'Dic'
        }
        month_spanish = months_in_spanish.get(month, month)
        return f'{day}/{month_spanish}/{year}'
    else:
        return None


def get_headlines(slug=None):
    items_data = []
    if slug is None:
        response = requests.get(BASE_URL)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            containers = soup.find_all(class_="zone__items")

            for container in containers:
                if container:
                    titles = container.find_all(class_="container__link--type-article")
                    
                    if titles:                    
                        for title in titles:
                            href = title['href']
                            date = extract_date_in_spanish(href)
                            title_extract = title.find_all(class_="container__headline-text")                            
                            for titlex in title_extract:
                                title = titlex.text
                                # img_src = container.find('source')
                                # img = edit_img(img_src['srcset'])
                                items_data.append({
                                    'id': '',
                                    'title': title,
                                    'date': date,
                                    'summary': '', 
                                    'body': '',
                                    'slug':  href,
                                    'cover': '',
                                    'url': DOMAIN + href
                                })

        return {"headlines": items_data,"code": CODE, "country": COUNTRY, "language": LANGUAGE}
    else:
        response = requests.get(BASE_URL + slug)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items_data = []
            if "seccion" in slug.lower():
                news = soup.find_all(class_="news__title")
                if not news:
                    other_format_news = soup.find_all('a', class_="container__link")
                    for new in other_format_news:
                        picture = new.find("picture")
                        if not picture:
                            title = new.text                                                              
                            href = new.get('href')                            
                            date = extract_date_in_spanish(href)
            
                            items_data.append({
                                'id': '',
                                'title': title,
                                'date': date,
                                'summary': '', 
                                'body': '',
                                'slug':  href,
                                'cover': '',
                                'url': DOMAIN + href
                            })
                    
                if news:                    
                    for new in news:
                        title = new.text
                        a = new.find('a')
                        href = a.get('href')
                        date = extract_date_in_spanish(href)
        
                        items_data.append({
                            'id': '',
                            'title': title,
                            'date': date,
                            'summary': '', 
                            'body': '',
                            'slug':  href,
                            'cover': '',
                            'url': DOMAIN + href
                        })
            else: # category
                news = soup.find_all(class_="container__link")                
                if news:
                    for new in news:
                        picture = new.find("picture")
                        if not picture:
                            title = new.text                            
                            href = new['href']
                            print(href)
                            date = extract_date_in_spanish(href)
            
                            items_data.append({
                                'id': '',
                                'title': title,
                                'date': date,
                                'summary': '', 
                                'body': '',
                                'slug':  href,
                                'cover': '',
                                'url': DOMAIN + href
                            })

            

            return {"headlines": items_data,"code": CODE, "country": COUNTRY, "language": LANGUAGE}

def get_categories():
    response = requests.get(BASE_URL)    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')   
        
        categories = soup.select('.header__nav-item-link')

        categories_object = []
        seen = set()        

        for cat in categories:
            text = cat.get_text(strip=True)
            href = cat.get('href')
            
            if text and href and (text, href) not in seen:
                if text != 'Video':
                    categories_object.append({                    
                        'label': text,
                        'slug': extract_categories_slug(href),                    
                    })
                    seen.add((text, href))

        return {
            "categories": categories_object,
        }


def get_content(slug):
    try:
        url = DOMAIN + "" + slug
        print(url)
        response = requests.get(url)    
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # TITLE
            header = soup.find('header', class_='storyfull__header')
            h1 = header.find('h1', class_='storyfull__title') if header else None            

            if not h1:
                h1 = soup.find('h1', id='maincontent')

            # BODY
            body = soup.find('div', class_='storyfull__body')            
            if not body:
                body = soup.find('main', class_='article__main')            
                
            content = []
            
            for tag in body.find_all(['p', 'h2']):        
                content.append({
                    'type': tag.name,
                    'text': tag.get_text().strip()
                })

            print(content)

            return {
                "title": h1.get_text(strip=True),
                "content": content,
                "url": url
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