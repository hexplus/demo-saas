import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(    
    api_key=os.getenv("OPENAI_API_KEY"),
)

def parse_json_content(content_list):
    parsed_text = ""    
    
    for item in content_list:        
        if isinstance(item, dict):
            text = item.get("text", "")
            content_type = item.get("type", "p")
            
            if content_type == "h2":
                parsed_text += f"## {text}\n\n"
            elif content_type == "p":
                parsed_text += f"{text}\n\n"
        else:
            print("Elemento no válido en content_list:", item)

    return parsed_text


def run_prompt(config):
    content = parse_json_content(config['content']['content'])
    prompt = f"Texto original: {content}\n\n"
    prompt += f"Traduce este texto a español si no está originalmente en ese idioma. \n"

    if config['summary']['status']:
        prompt += "Resume este texto. "
        prompt += f"El resumen debe ser de tipo {config['summary']['config']['type']}. "
        prompt += f"La longitud del resumen debe ser {config['summary']['config']['length']}.\n"

    if config['rephrase']['status']:
        prompt += "Reformula este texto para mejorar su comprensión y lectura. "
        prompt += f"Debe ser redactado con un estilo {config['rephrase']['config']['style']}. "
        prompt += f",con un tono {config['rephrase']['config']['tone']}. "
        prompt += f"y con un complejidad {config['rephrase']['config']['complexity']}.\n"

    
    print('Summary: ' + str(config['summary']['status']))
    print(config['summary']['config']['type'])
    print(config['summary']['config']['length'])
    print('Rephrase: ' + str(config['summary']['status']))    
    print(config['rephrase']['config']['style'])
    print(config['rephrase']['config']['tone'])
    print(config['rephrase']['config']['complexity'])
    



    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Actúa como una asistente especializada en periodismo, que ejecuta varias tareas. Tus respuestas deben reflejar estándares periodísticos, como precisión, objetividad y claridad. Sé concisa y precisa. Devuelve solo el texto procesado, no agregues mensajes adicionales ni indicaciones de lo que hiciste. Convierte el siguiente texto en una lista de diccionarios JSON donde cada párrafo sea un diccionario con las claves 'type' (siempre igual a 'p') y 'text' con el contenido del párrafo. Devuelve la respuesta en este formato JSON válido, con estos keys: 'title' para el título modificado por el AI,'content': para el contenido modificado por el AI y 'url' que sea un string vacío."},
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4-turbo",
    )

    output =  json.loads(response.choices[0].message.content)
    
    return output