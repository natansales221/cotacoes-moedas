import sqlite3
import os
import hashlib
import pandas as pd
from datetime import datetime

conn = sqlite3.connect(r"data\database\database.db")
cursor = conn.cursor()

cursor.execute("""DROP TABLE selic""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS selic(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    moeda TEXT NOT NULL,
    dt_cotacao TEXT,
    vl_cotacao TEXT,
    dt_carga,
    record_hash TEXT NOT NULL UNIQUE
)
""")

conn.commit()

path = r"data\downloads\selic"

def gerar_hash(row):

    conteudo = (
        f"{row['dt_cotacao']}|"
        f"{row['vl_cotacao']}|"
    )

    return hashlib.sha256(conteudo.encode("utf-8")).hexdigest()


for file_name in os.listdir(path):

    pasta_selic = os.path.join(path, file_name)
     
    if not os.path.isfile(pasta_selic):
        continue

    df = pd.read_csv(pasta_selic)

    if df.empty:
        print(f"{file_name} | arquivo vazio")
        continue
    
    df.rename(columns={"data": "dt_cotacao","valor": "vl_cotacao"},inplace=True)
    
    df["moeda"] = "Selic"
    df["dt_cotacao"] = pd.to_datetime(df["dt_cotacao"],format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
    df["record_hash"] = df.apply(gerar_hash,axis=1)
    df["dt_carga"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["vl_cotacao"] = df["vl_cotacao"].astype(float)

    df_load = df[
        [
            "moeda",
            "vl_cotacao",
            "dt_cotacao",
            "dt_carga",
            "record_hash"
        ]
    ]

    registros = list(df_load.itertuples(index=False,name=None))
    total_antes = conn.total_changes
    cursor.executemany("""
        INSERT OR IGNORE INTO selic (
            moeda,
            vl_cotacao,
            dt_cotacao,
            dt_carga,
            record_hash
        )
        VALUES (?, ?, ?, ?, ?)
    """, registros)

    conn.commit()

    inseridos = (conn.total_changes - total_antes)

    ignorados = (len(df_load) - inseridos)

    print(f"{file_name} | "f"lidos={len(df_load)} | "f"inseridos={inseridos} | "f"já existentes={ignorados}")


conn.close()