from flask import Flask, request, jsonify
import sqlite3
import os
import threading
from static.scripts.analytics_sender import send_to_google_analytics

app = Flask(__name__)

# Caminho do Banco de Dados
DATABASE = "database.db"


# Função para inicializar o banco de dados
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE projetos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            projeto TEXT NOT NULL,
                            url TEXT NOT NULL,
                            palavras_chave TEXT NOT NULL,
                            localizacao TEXT NOT NULL,
                            visitas_diarias INTEGER NOT NULL,
                            tempo_visita INTEGER NOT NULL,
                            measurement_id TEXT NOT NULL,
                            data_expiracao TEXT NOT NULL
                          )''')
        conn.commit()
        conn.close()


# Rota principal para teste
@app.route("/", methods=["GET"])
def home():
    return "Servidor Flask funcionando!"


# Rota para cadastrar os projetos
@app.route("/cadastrar-projeto", methods=["POST"])
def cadastrar_projeto():
    try:
        # Recebe os dados do formulário
        data = request.json
        projeto = data["projeto"]
        url = data["url"]
        palavras_chave = data["palavras_chave"]
        localizacao = data["localizacao"]
        visitas_diarias = int(data["visitas_diarias"])
        tempo_visita = int(data["tempo_visita"])
        measurement_id = data["measurement_id"]
        data_expiracao = data["data_expiracao"]

        # Salva os dados no banco de dados
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO projetos (projeto, url, palavras_chave, localizacao, 
                                                visitas_diarias, tempo_visita, measurement_id, 
                                                data_expiracao)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                       (projeto, url, palavras_chave, localizacao, visitas_diarias, tempo_visita, measurement_id,
                        data_expiracao))
        conn.commit()
        conn.close()

        # Inicia o envio dos dados ao Google Analytics em background
        threading.Thread(target=send_to_google_analytics,
                         args=(url, palavras_chave, localizacao, visitas_diarias, tempo_visita, measurement_id)).start()

        return jsonify({"status": "success", "message": "Projeto cadastrado com sucesso!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    init_db()  # Inicializa o banco de dados
    app.run(host="0.0.0.0", port=5000, debug=True)
