import passlib
import textwrap
import os
import google.generativeai as genai
from dotenv import load_dotenv


from IPython.display import display 
from IPython.display import Markdown

load_dotenv()

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

def prompt_gen(prompt, data):
    if not prompt or not isinstance(prompt, str):
        raise ValueError("Prompt must be a non-empty string")
    
    if not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    
    # Obtener preguntas y ponderaciones del diccionario
    preguntas = data.get("preguntas", [])
    ponderaciones = data.get("ponderaciones", [])
    
    # Formatear preguntas y ponderaciones como texto
    formatted_text = prompt + "\n"
    for pregunta, ponderacion in zip(preguntas, ponderaciones):
        formatted_text += f"P: {pregunta}, Ponderacion: {ponderacion}\n"

    # Generar contenido
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(formatted_text)
    to_markdown(response.text)
    return response.text
