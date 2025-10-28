from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

collection_name = "cepet"

client.create_collection(
  collection_name="cepet",
  vectors_config=VectorParams(size=1536, distance=Distance.DOT),
)

print(f"Se creó la colección: {collection_name}")