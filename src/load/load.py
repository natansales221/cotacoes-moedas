import sqlite3
import os
import hashlib
import pandas as pd
from datetime import datetime
from utils.utilidades import logs

conn = sqlite3.connect(r"data\database\database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moeda TEXT NOT NULL,
    cotacao_compra REAL,
    cotacao_venda REAL,
    dt_cotacao TEXT,
    hr_cotacao TEXT,
    tp_boletim TEXT,
    dt_carga TEXT,
    record_hash TEXT NOT NULL UNIQUE
)
""")

conn.commit()

path = r"data\downloads\ptax"

moedas = ["USD", "EUR", "GBP", "CHF", "JPY"]

def gerar_hash(row):
    conteudo = (
        f"{row['moeda']}|"
        f"{row['cotacao_compra']}|"
        f"{row['cotacao_venda']}|"
        f"{row['dt_cotacao']}|"
        f"{row['hr_cotacao']}|"
        f"{row['tp_boletim']}"
    )

    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()

for pasta_moeda in moedas:

    pasta_moedas = os.path.join(path, pasta_moeda)

    for file_name in os.listdir(pasta_moedas):

        caminho_arquivo = os.path.join(pasta_moedas, file_name)

        if not os.path.isfile(caminho_arquivo):
            continue

        if "USD" in file_name:
            moeda = "USD"
        elif "EUR" in file_name:
            moeda = "EUR"
        elif "GBP" in file_name:
            moeda = "GBP"
        elif "CHF" in file_name:
            moeda = "CHF"
        elif "JPY" in file_name:
            moeda = "JPY"
        else:
            continue

        df = pd.read_csv(caminho_arquivo)

        if df.empty:
            continue

        df["moeda"] = moeda

        df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
        df["dt_cotacao"] = (df["dataHoraCotacao"].dt.strftime("%Y-%m-%d"))
        df["hr_cotacao"] = (df["dataHoraCotacao"].dt.strftime("%H:%M:%S"))

        df.rename(columns={"cotacaoCompra": "cotacao_compra","cotacaoVenda": "cotacao_venda","tipoBoletim": "tp_boletim"},inplace=True)

        df["record_hash"] = df.apply(gerar_hash,axis=1)

        # Data da carga NÃO participa do hash.
        df["dt_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        df_load = df[["moeda", "cotacao_compra", "cotacao_venda", "dt_cotacao", "hr_cotacao", "tp_boletim", "dt_carga", "record_hash"]]

        registros = list(df_load.itertuples(index=False,name=None ))

        total_antes = conn.total_changes

        cursor.executemany("""
            INSERT OR IGNORE INTO currency (
                moeda,
                cotacao_compra,
                cotacao_venda,
                dt_cotacao,
                hr_cotacao,
                tp_boletim,
                dt_carga,
                record_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, registros)

        conn.commit()

        inseridos = conn.total_changes - total_antes
        ignorados = len(df_load) - inseridos

        print(f"{file_name} | "f"lidos={len(df_load)} | "f"inseridos={inseridos} | "f"já existentes={ignorados}")

conn.close()