from flask import Flask, request, jsonify
from consulta_tjrj import consultar_processo

app = Flask(__name__)

@app.route("/consulta", methods=["POST"])
def consulta():
    dados = request.get_json()
    numero = dados.get("numero_processo")
    if not numero:
        return jsonify({"erro": "Número do processo é obrigatório"}), 400
    resultado = consultar_processo(numero)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
    

@app.route('/')
def home():
    return "API Consulta Processual está no ar 🚀"

