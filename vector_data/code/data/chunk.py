from langchain_text_splitters import CharacterTextSplitter

def text_chunker(text):

  # Parametros para generar chunks
  text_splitter = CharacterTextSplitter(
    chunk_size=1100,
    chunk_overlap=50
  )

  # Chunks del texto
  chunks = text_splitter.split_text(text)

  return chunks
