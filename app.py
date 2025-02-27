from flask import Flask, request, render_template, jsonify
import os
import subprocess
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
LOG_FILE = 'logs.txt'  # Arquivo onde os logs serão salvos

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def escrever_log(mensagem):
    """Função para adicionar mensagens ao arquivo de log."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo inválido"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  

    escrever_log(f"🚀 Iniciando processamento do arquivo: {file.filename}")

    # Executa enviar_contatos.py e captura a saída em tempo real
    process = subprocess.Popen(
        ['python3', 'enviar_contatos.py', filepath], 
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    for line in iter(process.stdout.readline, ''):
        escrever_log(line.strip())  # Escreve cada linha de saída no log
        time.sleep(0.1)  # Pequeno delay para evitar bloqueio

    process.stdout.close()
    process.wait()

    return jsonify({"message": "Processamento iniciado!", "log_url": "/logs"})

@app.route('/logs', methods=['GET'])
def get_logs():
    """Retorna os logs armazenados no arquivo `logs.txt` de forma legível."""
    if not os.path.exists(LOG_FILE):
        return Response("Nenhum log disponível ainda.", mimetype="text/plain")

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read()

    # Retorna como texto simples, evitando caracteres Unicode codificados
    return Response(logs, mimetype="text/plain")

@app.route('/logs-page')
def logs_page():
    return render_template('logs.html')  # Exibe a página de logs