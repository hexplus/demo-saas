import requests
from bs4 import BeautifulSoup
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from helpers.helpers import fetch_all

PANIC_MODE = False
ADAPTER = "Acueductos y Alcantarillados"
TAG  = "AyA"
LANGUAGE = 'es-cr'
BASE_URL = 'https://websolutionss.aya.go.cr/WebNoticiasAYA/Home/DetalleNoticias?q=&desde=&hasta=&categoria=&etiqueta=&orden=des&astateNoticia=true&page='


PARENT_CONTAINER = 'divNoticias' # id
COVER_IMAGE = 'post-prev-img' # class
TITLE = 'post-prev-title'
LINK = 'h5.post-prev-title > a'


def page(id):
    print(id)
    # response = requests.get(BASE_URL + str(id))
    response = fetch_all([BASE_URL])


    # Verificar si la solicitud fue exitosa
    if response:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar el div con id "divNoticias"
        div_noticias = soup.find('div', id='divNoticias')

        if div_noticias:
            # Buscar todas las clases "post-prev-img" dentro del div "divNoticias"
            cover = div_noticias.find_all(class_=COVER_IMAGE)

            # Iterar sobre las noticias encontradas
            titulos = div_noticias.find_all('h5', class_='post-prev-title')

            # Iterar sobre los títulos encontrados
            for titulo in titulos:
                anchor = titulo.find('a')  # Buscar el anchor dentro del h5

                # Extraer el texto y el enlace del anchor
                texto_titulo = anchor.get_text(strip=True) if anchor else "Sin título"
                enlace = anchor['href'] if anchor and 'href' in anchor.attrs else "Sin enlace"

                # Manejo de enlaces relativos
                if not enlace.startswith('http'):
                    enlace = f"https://www.aya.go.cr{enlace}"
        else:
            print("No se encontró el div con id 'divNoticias'.")
    else:
        print(f"Error al acceder a la página. Código de estado: {response.status_code}")



page(1)