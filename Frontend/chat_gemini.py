from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

intructions = """
Eres un experto en temas legales chilenas, usando vocabulario correcto, y manteniendo siempre
la legalidad y el uso correcto de información entregada
"""

def chat(message, chunks):

  context = "\n".join(chunks)

  prompt = f"""
  Usando la siguiente información, de la mas relevante a la menor, contesta la siguiente pregunta en español:

  Contexto:
  {context}

  Pregunta:
  {message}
  """

  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
      system_instruction=intructions,
      temperature=0.2
    )
  )

  txt_result = response.text

  return txt_result