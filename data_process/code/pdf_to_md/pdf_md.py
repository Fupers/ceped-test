import os
import pymupdf4llm

path = "../../raw_data/"
files = os.listdir(path)

for file in files:
  print(f'Ejecutando: {file}')

  # Extraer texto del pdf
  pdf_path = path + file
  md_text = pymupdf4llm.to_markdown(pdf_path)

  md_name = file.split(".")[0] + ".md"
  md_path = "../../clean_data/" + md_name

  # Guardar texto en formato md
  with open(md_path, "a", encoding="utf-8") as f:
    f.write(md_text)

  print(f'Completado: {md_name}')
