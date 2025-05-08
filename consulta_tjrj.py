from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def consultar_processo_tjrj(numero_processo):
    url_busca = "https://www.tjrj.jus.br/web/guest/processos"

    # Configurações do Selenium em modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url_busca)

        # Espera carregar o iframe de busca de processos
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='consultaUnificada']"))
        )

        iframe = driver.find_element(By.CSS_SELECTOR, "iframe[src*='consultaUnificada']")
        driver.switch_to.frame(iframe)

        # Espera o campo do número do processo aparecer
        campo_numero = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "numeroProcesso"))
        )

        campo_numero.send_keys(numero_processo)

        # Clica no botão de pesquisar
        botao_pesquisar = driver.find_element(By.ID, "botaoConsultar")
        botao_pesquisar.click()

        # Espera os resultados carregarem
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "detalhe-processo"))
        )

        # Extrai as informações básicas
        assunto = driver.find_element(By.XPATH, "//div[contains(text(),'Assunto')]/following-sibling::div").text
        nome_parte = driver.find_element(By.XPATH, "//div[contains(text(),'Parte(s)')]/following-sibling::div").text
        situacao = driver.find_element(By.XPATH, "//div[contains(text(),'Situação')]/following-sibling::div").text

        # Última movimentação
        movimentacoes = driver.find_elements(By.CSS_SELECTOR, ".movimentacoes .movimentacao")
        ultima_movimentacao = movimentacoes[0].text if movimentacoes else "Não encontrado"

        return {
            "numero_processo": numero_processo,
            "nome_parte": nome_parte.strip(),
            "assunto": assunto.strip(),
            "situacao": situacao.strip(),
            "ultima_movimentacao": ultima_movimentacao.strip(),
        }

    except TimeoutException:
        return {"erro": "Tempo limite excedido ao consultar o processo."}
    except Exception as e:
        return {"erro": str(e)}
    finally:
        driver.quit()
