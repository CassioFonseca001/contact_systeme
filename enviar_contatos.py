import importlib  # Importar o módulo importlib

# Carregar os módulos
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
    "X-API-Key": "uliwgfxc19o8p00i1nsm67wa8hze0q3nqklek6vivdjwbgyd0lt1wz2uc1h8l7z0"  # Substitua pela sua chave real
}

# Variáveis para os campos adicionais
LOCALE = "pt"  # Locale fixo para todos

# Tenta carregar o arquivo CSV
try:
    df = pd.read_csv("contatos.csv")  # Certifique-se de que o arquivo está no mesmo diretório do script
except FileNotFoundError:
    print("Erro: O arquivo 'contatos.csv' não foi encontrado. Certifique-se de que ele está no mesmo diretório do script.")
    exit()

# Exibir colunas para depuração
print("Colunas encontradas no CSV:", df.columns.tolist())

# Normalizar os nomes das colunas (remover espaços extras, colocar minúsculas e substituir espaços por _)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Verificar se a coluna "email" existe
if "email" not in df.columns:
    print("Erro: A coluna 'Email' não foi encontrada no arquivo CSV. Colunas disponíveis:", df.columns.tolist())
    exit()

# Iterar sobre os emails e enviá-los para a API
for email in df["email"].dropna():
    payload = {
        "email": email,
        "locale": LOCALE
    }

    try:
        response = requests.post(URL, json=payload, headers=HEADERS)

        # Verifica se a API retornou sucesso (códigos 2xx)
        if response.status_code in range(200, 300):
            print(f"✅ Enviado com sucesso para {email} - Status: {response.status_code}")
        else:
            print(f"⚠️ Falha ao enviar {email} - Status: {response.status_code}, Erro: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar {email}: {e}")

print("🚀 Processo concluído!")