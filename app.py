from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota raiz para teste
@app.route('/')
def home():
    return "API Consulta Processual está no ar 🚀"

# Exemplo de rota futura para consulta processual (ainda a ser implementada)
@app.route('/consulta', methods=['GET'])
def consulta():
    return jsonify({"mensagem": "Aqui será feita a consulta pelo número do processo"}), 200

if __name__ == '__main__':
    app.run(debug=True)
