import json
import platform
import locale
import lzma
import base64

def get_adapters_by_country_code(country_code):    
    with open('./data/adapters.json', 'r', encoding='utf-8') as file:
        adapters = json.load(file)
        result = []
        for adapter in adapters:
            if adapter['country'] == country_code or adapter['country'] == 'INT':
                result.append(adapter)
        return result
    

def get_adapters():
    with open('./data/adapters.json', 'r', encoding='utf-8') as file:
        adapters = json.load(file)        
        adapters_sorted = sorted(adapters, key=lambda x: x['name'])
        return adapters_sorted

def get_styles():
    with open('./data/styles.json', 'r', encoding='utf-8') as file:
        styles = json.load(file)                
        return styles
    
def get_tones():
    with open('./data/tones.json', 'r', encoding='utf-8') as file:
        tones = json.load(file)                
        return tones
    
def get_complexities():
    with open('./data/complexities.json', 'r', encoding='utf-8') as file:
        complexities = json.load(file)                
        return complexities
    
def get_summary_types():
    with open('./data/summary_types.json', 'r', encoding='utf-8') as file:
        summary_types = json.load(file)                
        return summary_types
    
def get_social_networks():
    with open('./data/social_networks.json', 'r', encoding='utf-8') as file:
        social_networks = json.load(file)                
        return social_networks

def get_summary_lengths():
    with open('./data/summary_lengths.json', 'r', encoding='utf-8') as file:
        summary_lengths = json.load(file)                
        return summary_lengths

# FOR ICE URLS
def extract_slug(url):
    # Patrón redundante
    base_pattern = "/wps/portal/ICE/quienessomos/sala-prensa/sala-de-prensa/noticias/"
    
    # Verificamos si la URL empieza con el patrón
    if url.startswith(base_pattern):
        # Remover el patrón inicial y retornar el slug
        return url[len(base_pattern):]
    else:
        return url  # Si la URL no tiene el patrón, retornamos la URL completa