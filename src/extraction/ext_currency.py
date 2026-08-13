from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
import logging
from src.utils.utilidades import logs

class Extraction():
    # URL to search currency
    def url():
        return "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"

    # Extracting wished currency since 2000's
    def main(self, moedas, arquivo_log):
        logger = logging.getLogger(__name__)
        
        logger.info("=" * 60)
        logger.info("INÍCIO DA EXTRAÇÃO PTAX")
        logger.info(f"Arquivo de log: {arquivo_log}")
        logger.info("=" * 60)
        
        ano_atual = datetime.now().year

        for moeda in moedas:
            for ano in range(2000, ano_atual + 1):
                logger.info("=" * 60)
                logger.info(f"Iniciando extração: moeda={moeda}, ano={ano}")
                PARAMS = {
                    "@moeda": f"'{moeda}'",
                    "@dataInicial": f"'01-01-{ano}'",
                    "@dataFinalCotacao": f"'12-31-{ano}'",
                    "$top": 100000,
                    "$format": "json",
                    "$select": "cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
                }

                response = requests.get(Extraction.url(), params=PARAMS, timeout=30)
                response.raise_for_status()
                logger.info(f"Consulta feita com sucesso!")
                dados = response.json()["value"]

                df = pd.DataFrame(dados)
                
                logger.info(f"Dataframe criado com sucesso")
                
                destino = Path(f"data/downloads/ptax/{moeda}")
                destino.mkdir(parents=True, exist_ok=True)
                logger.info(f"Pasta criada com sucesso")
                arquivo = destino / f"ptax_{moeda}_{ano}.csv"

                df.to_csv(arquivo, index=False, encoding="utf-8")
                
                logger.info("Extração concluída")
                logger.info(f"Foram extraídos {len(df)} registros")
                logger.info("=" * 60)

        logger.info("=" * 60)
        logger.info("FIM DA EXTRAÇÃO PTAX")
        logger.info("=" * 60)
    
if __name__ == "__main__":
    service=Extraction()
    lista_moedas = ["AUD", "CAD", "CHF", "DKK", "EUR", "GBP", "JPY", "NOK", "SEK", "USD"]
    arquivo = logs()
    service.main(moedas=lista_moedas, arquivo_log=arquivo)
    
