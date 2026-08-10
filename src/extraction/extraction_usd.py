from pathlib import Path
from datetime import datetime
import pandas as pd
import requests

ano_atual = datetime.now().year
data_hoje = datetime.now().strftime("%m-%d-%Y")

URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
)
for ano in range(2000, ano_atual + 1):
    PARAMS = {
        "@dataInicial": f"'01-01-{ano}'",
        "@dataFinalCotacao": f"'12-31-{ano}'",
        "$top": 10000,
        "$format": "json",
        "$select": "cotacaoCompra,cotacaoVenda,dataHoraCotacao",
    }


    response = requests.get(URL, params=PARAMS, timeout=30)
    response.raise_for_status()

    dados = response.json()["value"]

    df = pd.DataFrame(dados)

    destino = Path("data/downloads/ptax/USD")
    destino.mkdir(parents=True, exist_ok=True)

    arquivo = destino / f"ptax_USD_{ano}.csv"

    df.to_csv(arquivo, index=False, encoding="utf-8")

    print(f"Extração concluída.")
    print(f"Registros extraídos: {len(df)}")
    print(f"Arquivo criado: {arquivo}")