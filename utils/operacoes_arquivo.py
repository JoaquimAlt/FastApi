import os
import zipfile
import hashlib

ARQUIVO_CSV = "mesas.csv"
ARQUIVO_ZIP = "mesas.zip"

# Compactar o arquivo CSV
def compactar_csv():
    with zipfile.ZipFile(ARQUIVO_ZIP, mode="w", compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(ARQUIVO_CSV, os.path.basename(ARQUIVO_CSV))

# Calcular o hash SHA256 do arquivo CSV
def calcular_hash_csv() -> str:
    sha256 = hashlib.sha256()
    with open(ARQUIVO_CSV, mode="rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
