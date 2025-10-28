from chunk import text_chunker
from dotenv import load_dotenv
from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from datetime import datetime
import os
import json
import uuid

load_dotenv()
client = genai.Client()
client_gdrant = QdrantClient(url="http://localhost:6333")

# Obtener texto del md
def get_text(path):

  with open(path, "r", encoding="utf-8") as f:
    text = f.read()
  
  return text

# Generar un embedding de un texto
def get_embedding(text):

  result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=text,
    config=types.EmbedContentConfig(output_dimensionality=1536)
  )

  vector = result.embeddings[0].values
  return vector

def update_historial(temp):

  path = "/home/krypto/home/cepet-app/vector_data/code/data/historial.json"

  historial_json = []
  if os.path.exists(path):
    try:
      with open(path, "r", encoding="utf-8") as f:
        historial_json = json.load(f)

    except json.JSONDecodeError:
      historial_json = []

  historial_json.extend(temp)

  with open(path, "w", encoding="utf-8") as f:
    json.dump(historial_json, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
  init_path = "/home/krypto/home/cepet-app/data_process/clean_data/"
  file_name = "reso146_2025.md"
  collection_name = "cepet"
  path = init_path + file_name

  text = get_text(path)
  chunks = text_chunker(text)

  points = []
  historial_temp = []

  for index, chunk in enumerate(chunks):
    point_id = str(uuid.uuid4())
    print(f"Procesando punto: {point_id}")
    vector = get_embedding(chunk)
    points.append(PointStruct(id=point_id, vector=vector, payload={"text": chunk}))

    historial_temp.append({
      "id": point_id,
      "chunk_index": index,
      "file_name": file_name,
      "collection": collection_name,
      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

  operation_info = client_gdrant.upsert(
    collection_name=collection_name,
    wait=True,
    points=points
  )

  update_historial(historial_temp)
  print("\nProceso completado, guardado en historial")

  

  