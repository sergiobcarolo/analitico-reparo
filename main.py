"""Orquestrador principal do Analítico Reparo."""

import os
import sys
import logging
import pandas as pd

# Adiciona o diretório raiz ao path para importar os módulos de src/ e config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from src.select_files import selecionar_arquivo
from src.filters import aplicar_filtro_base, filtrar_injecao, filtrar_cancelamento
from src.analytics import gerar_resumo
from src.generate_files import gerar_arquivo_injecao, gerar_arquivo_cancelamento

# ─── Configuração do Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def validar_colunas(df: pd.DataFrame) -> None:
    """Verifica se todas as colunas obrigatórias estão presentes no DataFrame.

    Args:
        df: DataFrame lido do Excel de entrada.

    Raises:
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """
    faltando = [c for c in config.COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(
            f"Colunas não encontradas no arquivo: {faltando}\n"
            f"Colunas disponíveis: {list(df.columns)}"
        )


def main():
    try:
        # 1. Seleção do arquivo
        caminho = selecionar_arquivo()
        if caminho is None:
            log.warning("Nenhum arquivo selecionado. Encerrando.")
            return

        # 2. Leitura do Excel
        log.info("Lendo arquivo...")
        df = pd.read_excel(caminho)
        log.info("Registros lidos: %d", len(df))

        # 3. Validação de colunas
        validar_colunas(df)

        # 4. Filtros
        df_filtrado    = aplicar_filtro_base(df)
        df_injecao     = filtrar_injecao(df_filtrado)
        df_cancelamento = filtrar_cancelamento(df_filtrado)

        # 5. Analíticos
        gerar_resumo(df_injecao, df_cancelamento)

        # 6. Criação da pasta de saída
        pasta_saida = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), config.PASTA_SAIDA
        )
        os.makedirs(pasta_saida, exist_ok=True)

        # 7. Geração dos arquivos
        gerar_arquivo_injecao(df_injecao, pasta_saida)
        gerar_arquivo_cancelamento(df_cancelamento, pasta_saida)

        log.info("Processo finalizado com sucesso! Arquivos em: %s", pasta_saida)

    except ValueError as e:
        # Erros de validação de negócio (ex: coluna ausente)
        log.error("Erro de validação: %s", e)
        sys.exit(1)

    except FileNotFoundError as e:
        log.error("Arquivo não encontrado: %s", e)
        sys.exit(1)

    except Exception as e:
        # Qualquer outro erro inesperado
        log.exception("Erro inesperado: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()