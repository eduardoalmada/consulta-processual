
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

@app.route("/consultar", methods=["POST"])
def consultar_processo():
    numero_processo = request.json.get("numero_processo")

    if not numero_processo:
        return jsonify({"erro": "Número do processo não fornecido"}), 400

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.tjrj.jus.br/web/guest/processos")

        time.sleep(2)

        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='consultaprocessual']")
        driver.switch_to.frame(iframe)

        campo_processo = driver.find_element(By.ID, "txtNumeroProcesso")
        campo_processo.send_keys(numero_processo)

        botao_pesquisar = driver.find_element(By.ID, "btnPesquisar")
        botao_pesquisar.click()

        time.sleep(6)

        resultado = driver.find_element(By.ID, "lblCabecalho").text
        situacao = driver.find_element(By.ID, "lblSituacaoProcesso").text
        movimentacao = driver.find_element(By.ID, "lblUltimaMovimentacao").text
        assunto = driver.find_element(By.ID, "lblAssunto").text
        parte = driver.find_element(By.ID, "lblPartes").text

        return jsonify({
            "numero_processo": numero_processo,
            "nome_parte": parte,
            "assunto": assunto,
            "situacao": situacao,
            "ultima_movimentacao": movimentacao,
            "resumo": resultado
        })

    except Exception as e:
        return jsonify({"erro": f"Erro ao consultar: {str(e)}"}), 500
    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
