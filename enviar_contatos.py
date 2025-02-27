import sys  # Para capturar o nome do arquivo via argumento
import importlib
import requests
import pandas as pd
import openpyxl

# Recarregar os módulos
importlib.reload(requests)
importlib.reload(pd)
importlib.reload(openpyxl)

# Configuração da API
URL = "https://api.systeme.io/api/contacts"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-Key": "uliwgfxc19o8p00i1nsm67wa8hze0q3nqklek6vivdjwbgyd0lt1wz2uc1h8l7z0"
}

LOCALE = "pt"  # Locale fixo para todos

# 🔹 Lendo o nome do arquivo CSV a partir do argumento
if len(sys.argv) < 2:
    print("Erro: Nenhum arquivo CSV especificado.")
    sys.exit(1)

csv_file = sys.argv[1]  # Nome do arquivo passado como argumento pelo `app.py`

# 🔹 Tentando carregar o arquivo CSV correto
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Erro: O arquivo '{csv_file}' não foi encontrado.")
    sys.exit(1)

# Exibir colunas para depuração
print("Colunas encontradas no CSV:", df.columns.tolist())

# Normalizar os nomes das colunas
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Verificar se a coluna "email" existe
if "email" not in df.columns:
    print("Erro: A coluna 'Email' não foi encontrada no arquivo CSV.")
    sys.exit(1)

# 🔹 Processamento dos emails
for email in df["email"].dropna():
    payload = {
        "email": email,
        "locale": LOCALE,
        "fields": [
            {"slug": "tags", "value": "Contatos-Site"}
        ]
    }

    response = requests.post(URL, json=payload, headers=HEADERS)

    if response.status_code == 422:
        print(f"⚠️ Falha ao enviar {email} - Status: 422 - Este email já existe.")
    else:
        print(f"✅ Enviado com sucesso para {email} - Status: {response.status_code}")

print("🚀 Processo concluído!")