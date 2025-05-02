from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota principal de teste
@app.route('/')
def home():
    return 'API Consulta Processual TJRJ funcionando!'

# Rota de consulta simulada (substituir depois por scraping real)
@app.route('/consultar', methods=['POST'])
def consultar():
    dados = request.get_json()
    numero_processo = dados.get('numero_processo')

    if not numero_processo:
        return jsonify({'erro': 'Número do processo não fornecido'}), 400

    # Simulação de retorno (será substituído pela consulta real ao TJRJ)
    resultado = {
        'numero_processo': numero_processo,
        'nome_parte': 'Fulano de Tal',
        'assunto': 'Danos Morais',
        'situacao': 'Em Andamento',
        'ultima_movimentacao': 'Petição Juntada - 25/04/2025'
    }

    return jsonify(resultado)
