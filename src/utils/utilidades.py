from pathlib import Path
from datetime import datetime
import logging

def logs():
    agora = datetime.now()

    data_execucao = agora.strftime("%Y-%m-%d")
    hora_execucao = agora.strftime("%H%M%S")

    pasta_logs = Path("logs") / data_execucao
    pasta_logs.mkdir(parents=True, exist_ok=True)

    arquivo_log = pasta_logs / f"extraction_{hora_execucao}.log"

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[
                            logging.FileHandler(arquivo_log, encoding="utf-8"),
                            logging.StreamHandler()
                            ]
                        )
    return arquivo_log