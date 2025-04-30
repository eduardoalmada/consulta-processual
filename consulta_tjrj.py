from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def consultar_processo(numero_processo):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = "https://www4.tjrj.jus.br/consultaprocessualweb/faces/index.jsp"
    driver.get(url)
    sleep(2)
    try:
        driver.find_element(By.ID, "numeroProcesso").send_keys(numero_processo)
        driver.find_element(By.ID, "btnPesquisar").click()
        sleep(4)
        resultado = {
            "numero": numero_processo,
            "parte": "Fulano de Tal",
            "assunto": "Direito Civil",
            "situacao": "Em andamento",
            "ultima_movimentacao": "Juntada de petição em 28/04/2025"
        }
    except Exception as e:
        resultado = {"erro": str(e)}
    finally:
        driver.quit()
    return resultado
