import sqlite3
import os
import pandas as pd
import sqlite3

# Conectando ao banco de dados SQLite
conn = sqlite3.connect(r'data\database\database.db')
path = r'data\downloads\ptax'

for file_name in os.listdir(path):
    # Verificando se o item na pasta é um arquivo (e não uma pasta)
    if os.path.isfile(os.path.join(path, file_name)):
        if file_name[16:22] == "nomegenerico":
            df = pd.read_excel(os.path.join(path, file_name))
            # Inserindo os dados do dataframe na tabela do banco de dados SQLite
            df.to_sql(file_name[:29], conn, if_exists='replace', index=False)
            # Imprimindo uma mensagem informando que os dados foram inseridos com sucesso
            print(f"Dados de {file_name} inseridos com sucesso na tabela {file_name}")
        elif file_name[16:22] == "nomegenerico":
            df = pd.read_excel(os.path.join(path, file_name))
            # Inserindo os dados do dataframe na tabela do banco de dados SQLite
            df.to_sql(file_name[:28], conn, if_exists='replace', index=False)
            # Imprimindo uma mensagem informando que os dados foram inseridos com sucesso
            print(f"Dados de {file_name} inseridos com sucesso na tabela {file_name}")
        else:
            print("vai ser ignorada")

conn.close()  
        
f = False