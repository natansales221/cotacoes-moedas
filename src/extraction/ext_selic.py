import requests
import os
import csv
from datetime import datetime
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados"

PERIODOS = [
    ("01/01/2000", "31/12/2009"),
    ("01/01/2010", "31/12/2019"),
    ("01/01/2020", "31/12/2026")
]

diretorio = r'D:\Desktop\Projetos\cotacoes-moedas\data\downloads\selic'
todos_dados = []

for data_inicial, data_final in PERIODOS:

    print(f"Consultando: {data_inicial} até {data_final}")

    parametros = {"formato": "json","dataInicial": data_inicial,"dataFinal": data_final}

    resposta = requests.get(URL,params=parametros, headers={"User-Agent": "Mozilla/5.0"})

    if resposta.status_code != 200:
        print(f"Erro na consulta: {resposta.status_code}")
        print(resposta.text)
        exit()

    dados = resposta.json()

    todos_dados.extend(dados)

    print(f"Registros encontrados: {len(dados)}")


arquivo = "selic.csv"
os.makedirs(diretorio, exist_ok=True)

caminho_arquivo = os.path.join(diretorio, arquivo)

df = pd.DataFrame(todos_dados)
df.to_csv(caminho_arquivo, index=False, encoding="utf-8")

print("CSV criado com sucesso!")
print(f"Total de registros: {len(todos_dados)}")
