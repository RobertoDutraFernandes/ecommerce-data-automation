from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from email.message import EmailMessage
import smtplib
import pandas as pd
import os
import time

# ========== Credenciais para login do Email ==========
EMAIL = "roberto.filho.mrm75@gmail.com"
SENHA = "ppbw jnzr bgzt srxj" 

# ========== Funções Principais ==========

# Função responsável por abrir o navegador na url passada em tela cheia
def iniciar_navegador():
    navegador = webdriver.Chrome()
    url = "https://www.magazineluiza.com.br/"
    for _ in range(3):
        try:
            navegador.get(url)
            WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.ID, "input-search"))
            )
            print("Página carregada com sucesso.")
            break
        except:
            time.sleep(1)
    else:
        print("Site fora do ar")
        navegador.quit()
        exit()
    navegador.maximize_window()
    return navegador

# Função responsável por pesquisar "notebooks" na barra de busca do site
def buscar_produto(navegador, termo="notebooks"):
    barra_busca = navegador.find_element(By.ID, "input-search")
    barra_busca.send_keys(termo)
    barra_busca.send_keys(Keys.ENTER)

# Função responsável por captar as informações dos produtos na página atual
def capturar_info(navegador, produtos, avaliacoes, urls):
    i = 1
    time.sleep(4)
    while True:
        try:
            nome_xpath = f"//ul[@data-testid='list']/li[{i}]//a//div[@data-testid='product-card-content']//h2"
            aval_xpath = f"//ul[@data-testid='list']/li[{i}]//a//div[@data-testid='product-card-content']//div[@class='sc-kSsbVf hYgbCw']/div/span"
            url_xpath = f"//ul[@data-testid='list']/li[{i}]//a"

            nome_elementos = navegador.find_elements(By.XPATH, nome_xpath)
            if not nome_elementos:
                break

            nome = nome_elementos[0].text
            aval_elementos = navegador.find_elements(By.XPATH, aval_xpath)
            aval = aval_elementos[0].text if aval_elementos else "Sem avaliação"
            url = navegador.find_element(By.XPATH, url_xpath).get_attribute("href")

            produtos.append(nome)
            avaliacoes.append(aval)
            urls.append(url)

            i += 1
            time.sleep(0.1)
        except Exception as e:
            print(f"Erro no item {i}: {e}")
            break

# Função responsável por localizar o botão de passar de página e avançar enquanto houver páginas seguintes
def navegar_pelas_paginas(navegador, produtos, avaliacoes, urls):
    while True:
        capturar_info(navegador, produtos, avaliacoes, urls)
        try:
            botao_proximo = navegador.find_element(
                By.XPATH, "//*[@id='__next']/div/main/section[4]/div[6]/nav/ul/li[9]/button"
            )
            if not botao_proximo.is_enabled():
                print("Última página.")
                break
            navegador.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
            time.sleep(1)
            botao_proximo.click()
            time.sleep(4)
        except (NoSuchElementException, ElementClickInterceptedException):
            print("Botão 'Próxima' não encontrado ou inativo.")
            break

# Função responsável por transformar os dados obtidos em DataFrame e posteriormente em uma planilha excel
def exportar_para_excel(produtos, avaliacoes, urls, nome_arquivo="Output/Notebooks.xlsx"):
    os.makedirs("Output", exist_ok=True)
    df = pd.DataFrame({
        "PRODUTO": produtos,
        "QTD_AVAL": avaliacoes,
        "URL": urls
    })

    df_filtrado = df[df["QTD_AVAL"] != "Sem avaliação"].copy()
    df_filtrado["QTD_AVAL"] = df_filtrado["QTD_AVAL"].str.extract(r'\((\d+)\)').astype(int)

    melhores = df_filtrado[df_filtrado["QTD_AVAL"] >= 100]
    piores = df_filtrado[df_filtrado["QTD_AVAL"] < 100]

    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        melhores.to_excel(writer, sheet_name="Melhores", index=False)
        piores.to_excel(writer, sheet_name="Piores", index=False)

    print(f"Excel exportado para: {nome_arquivo}")
    return nome_arquivo

# Função responsável por preencher o email e enviar o arquivo excel gerado
def enviar_email_com_arquivo(arquivo, remetente, senha):
    msg = EmailMessage()
    msg['Subject'] = 'Relatório Notebooks'
    msg['From'] = remetente
    msg['To'] = remetente
    msg.set_content("Olá, aqui está o seu relatório dos notebooks \nextraídos da Magazine Luiza.\n\nAtenciosamente,\nRobô")

    with open(arquivo, 'rb') as f:
        conteudo = f.read()
        msg.add_attachment(conteudo, maintype='application', subtype='octet-stream', filename=os.path.basename(arquivo))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)

    print("E-mail enviado com sucesso.")

# ========== Main ==========

# Programa principal, responsável por executar as funções criadas anteriormente 
def main():
    produtos = []
    avaliacoes = []
    urls = []

    navegador = iniciar_navegador()
    buscar_produto(navegador)
    navegar_pelas_paginas(navegador, produtos, avaliacoes, urls)
    navegador.quit()

    caminho_excel = exportar_para_excel(produtos, avaliacoes, urls)
    enviar_email_com_arquivo(caminho_excel, EMAIL, SENHA)

if __name__ == "__main__":
    main()
