from flask import Flask, request, render_template, jsonify
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Garante que a pasta de uploads exista

@app.route('/')
def upload_form():
    return render_template('upload.html')  # Renderiza a página de upload

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome do arquivo inválido"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  # Salva o arquivo CSV no servidor

    # 🔹 Executa o script enviar_contatos.py passando o caminho do arquivo CSV
    result = subprocess.run(['python3', 'enviar_contatos.py', filepath], capture_output=True, text=True)

    return jsonify({"message": "Arquivo processado!", "output": result.stdout, "error": result.stderr})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)