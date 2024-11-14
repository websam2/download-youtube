from flask import Flask, render_template, request, jsonify, send_from_directory
from downloader import download_playlist
import threading
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DOWNLOAD_FOLDER = 'downloads'  # Diretório onde os vídeos são armazenados

# Garante que o diretório de downloads exista
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def start_download():
    url = request.json.get('url')
    try:
        # Inicia o download em uma nova thread para não bloquear a aplicação
        threading.Thread(target=download_playlist, args=(url,)).start()
        return jsonify({"message": "Download iniciado"}), 202
    except Exception as e:
        logging.error(f"Erro ao iniciar o download: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Endpoint para listar todos os vídeos baixados
@app.route('/list-downloads', methods=['GET'])
def list_downloads():
    try:
        files = os.listdir(DOWNLOAD_FOLDER)
        videos = [{'filename': file} for file in files if file.endswith('.mp4')]
        return jsonify({'videos': videos})
    except Exception as e:
        logging.error(f"Erro ao listar os vídeos: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Endpoint para servir arquivos de vídeo para download
@app.route('/downloads/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Erro ao enviar arquivo: {str(e)}")
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)
