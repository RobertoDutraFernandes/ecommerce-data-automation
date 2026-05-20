# Notebook Web Scraping RPA

Automação desenvolvida em Python utilizando Selenium para extração de informações de notebooks no site da Magazine Luiza.

O robô realiza automaticamente:
- abertura do navegador
- pesquisa de produtos
- extração de dados
- navegação entre páginas
- geração de relatório Excel
- envio automático do relatório por e-mail

---

# Tecnologias Utilizadas

- Python
- Selenium
- Pandas
- OpenPyXL
- SMTP
- Web Scraping
- Automação RPA

---

# Funcionalidades

## Verificação de disponibilidade do site
O robô verifica se o site carregou corretamente.
Caso haja falha, são realizadas até 3 tentativas automaticamente.

---

## Pesquisa automática
O sistema pesquisa automaticamente por notebooks na barra de busca.

---

## Extração de dados
São capturados:
- Nome do produto
- Quantidade de avaliações
- URL do produto

---

## Paginação automática
O robô navega automaticamente entre as páginas para coletar mais produtos.

---

## Geração de relatório Excel
Os dados são organizados automaticamente em:
- Aba "Melhores" → produtos com 100+ avaliações
- Aba "Piores" → produtos com menos de 100 avaliações

---

## Envio automático por e-mail
Ao finalizar o processo, o relatório é enviado automaticamente por e-mail.

---

# Como Executar

## 1. Clone o repositório

```bash
git clone https://github.com/seuusuario/notebook-web-scraping-rpa.git
```

## 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 3. Execute o projeto

```bash
python main.py
```

---

# Dependências

```txt
selenium
pandas
openpyxl
```

---

# Aprendizados

Este projeto permitiu praticar:
- Automação de processos (RPA)
- Web Scraping
- Manipulação de dados
- Geração automatizada de relatórios
- Integração com e-mail SMTP
- Tratamento de exceções
- Navegação automatizada com Selenium

---

# Autor

Roberto Dutra Fernandes Filho
