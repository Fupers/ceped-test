from dotenv import load_dotenv
from google import genai
from google.genai import types
from qdrant_client import QdrantClient, models

load_dotenv()
client = genai.Client()
client_qdrant = QdrantClient(url="http://localhost:6333")

# Generar un embedding de un texto
def get_embedding(text):
  result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
    config=types.EmbedContentConfig(output_dimensionality=1536)
  )

  vector = result.embeddings[0].values
  return vector

# Obtener los mejores resultados de la colección
def query(vector):
  search_result = client_qdrant.query_points(
    collection_name="cepet",
    query=vector,
    limit=5,
    with_payload=True
  ).points

  return search_result

def generative(message):

  vector = get_embedding(message)
  result = query(vector)
  texts = [point.payload["text"] for point in result]

  return texts
