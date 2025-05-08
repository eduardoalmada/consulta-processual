from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

@app.route('/consultar', methods=['POST'])
def consultar_processo():
    dados = request.get_json()
    numero_processo = dados.get("numero_processo")

    if not numero_processo:
        return jsonify({"erro": "Número do processo não fornecido"}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get("https://www.tjrj.jus.br/web/guest/processos")

        # Esperar campo de número do processo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "numeroProcesso"))
        )

        # Preencher número e pesquisar
        input_campo = driver.find_element(By.ID, "numeroProcesso")
        input_campo.clear()
        input_campo.send_keys(numero_processo)

        botao = driver.find_element(By.ID, "botaoPesquisar")
        botao.click()

        # Esperar resultado carregar
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "detalhes-processo"))
        )

        # Extração dos dados
        nome_parte = driver.find_element(By.XPATH, "//div[contains(text(),'Partes')]/following-sibling::div").text
        assunto = driver.find_element(By.XPATH, "//div[contains(text(),'Assunto')]/following-sibling::div").text
        situacao = driver.find_element(By.XPATH, "//div[contains(text(),'Situação')]/following-sibling::div").text
        ultima_mov = driver.find_element(By.XPATH, "//div[contains(text(),'Última Movimentação')]/following-sibling::div").text

        driver.quit()

        return jsonify({
            "numero_processo": numero_processo,
            "nome_parte": nome_parte,
            "assunto": assunto,
            "situacao": situacao,
            "ultima_movimentacao": ultima_mov
        })

    except Exception as e:
        driver.quit()
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
