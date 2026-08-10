from pathlib import Path
from datetime import datetime
import pandas as pd
import requests
import logging


ano_atual = datetime.now().year
data_hoje = datetime.now().strftime("%m-%d-%Y")

moedas = ["USD", "EUR", "GBP", "CHF", "JPY"]

# Momento da execução
agora = datetime.now()

data_execucao = agora.strftime("%Y-%m-%d")
hora_execucao = agora.strftime("%H%M%S")

# logs/2026-08-10/
pasta_logs = Path("logs") / data_execucao
pasta_logs.mkdir(parents=True, exist_ok=True)

# logs/2026-08-10/extraction_162530.log
arquivo_log = pasta_logs / f"extraction_{hora_execucao}.log"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                    handlers=[
                        logging.FileHandler(arquivo_log, encoding="utf-8"),
                        logging.StreamHandler()
                        ]
                    )

logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("INÍCIO DA EXTRAÇÃO PTAX")
logger.info(f"Arquivo de log: {arquivo_log}")
logger.info("=" * 60)

URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
)
for moeda in moedas:
    for ano in range(2000, ano_atual + 1):
        logger.info("=" * 60)
        logger.info(f"Iniciando extração: moeda={moeda}, ano={ano}")
        PARAMS = {
            "@moeda": f"'{moeda}'",
            "@dataInicial": f"'01-01-{ano}'",
            "@dataFinalCotacao": f"'12-31-{ano}'",
            "$top": 10000,
            "$format": "json",
            "$select": "cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
        }

        response = requests.get(URL, params=PARAMS, timeout=30)
        response.raise_for_status()
        logger.info(f"Consulta feita com sucesso!")
        dados = response.json()["value"]

        df = pd.DataFrame(dados)
        
        logger.info(f"Dataframe criado com sucesso")
        
        destino = Path(f"data/downloads/ptax/teste/{moeda}")
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