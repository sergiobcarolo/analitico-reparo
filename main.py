"""Orquestrador principal do Analítico Reparo."""

import os
import sys
import logging
import pandas as pd

# Adiciona o diretório raiz ao path para importar os módulos de src/ e config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from src.select_files import selecionar_arquivos_entrada
from src.filters import (
    filtrar_gpon_injecao,
    filtrar_metalico_injecao,
    filtrar_ordens_excedentes,
)
from src.analytics import gerar_resumo_consolidado
from src.generate_files import (
    gerar_arquivo_injecao,
    gerar_arquivo_cancelamento,
)

# ─── Configuração do Logging ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


def _validar_colunas(df: pd.DataFrame, colunas_esperadas: list[str], tipo_arquivo: str) -> None:
    """Verifica se todas as colunas obrigatórias estão presentes no DataFrame.

    Args:
        df: DataFrame lido da planilha Excel.
        colunas_esperadas: Lista com as colunas requeridas.
        tipo_arquivo: Nome descritivo do arquivo (ex: 'GPON' ou 'METÁLICO').

    Raises:
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """
    faltando = [c for c in colunas_esperadas if c not in df.columns]
    if faltando:
        raise ValueError(
            f"Colunas obrigatórias ausentes no arquivo {tipo_arquivo}: {faltando}\n"
            f"Colunas disponíveis: {list(df.columns)}"
        )


def _obter_pasta_saida() -> str:
    """Cria e retorna o caminho absoluto da pasta de saída."""
    pasta = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), config.PASTA_SAIDA
    )
    os.makedirs(pasta, exist_ok=True)
    return pasta


def main():
    try:
        # 1. Seleção conjunta dos arquivos GPON e METÁLICO
        arquivos = selecionar_arquivos_entrada()
        if arquivos is None:
            log.warning("Seleção cancelada pelo usuário. Encerrando.")
            return

        caminho_gpon = arquivos["gpon"]
        caminho_metalico = arquivos["metalico"]

        # 2. Leitura dos arquivos Excel
        log.info("Lendo arquivo GPON: %s", caminho_gpon)
        df_gpon = pd.read_excel(caminho_gpon)
        log.info("Registros lidos (GPON): %d", len(df_gpon))

        log.info("Lendo arquivo METÁLICO: %s", caminho_metalico)
        df_metalico = pd.read_excel(caminho_metalico)
        log.info("Registros lidos (METÁLICO): %d", len(df_metalico))

        # 3. Validação das colunas obrigatórias
        _validar_colunas(df_gpon, config.COLUNAS_OBRIGATORIAS_GPON, "GPON")
        _validar_colunas(df_metalico, config.COLUNAS_OBRIGATORIAS_METALICO, "METÁLICO")

        # 4. Aplicação dos filtros de injeção e visitas excedentes
        df_gpon_inj = filtrar_gpon_injecao(df_gpon)
        df_met_inj = filtrar_metalico_injecao(df_metalico)
        df_excedentes = filtrar_ordens_excedentes(df_gpon, df_metalico)

        # 5. Apresentação do resumo analítico consolidado
        gerar_resumo_consolidado(df_gpon_inj, df_met_inj, df_excedentes)

        # 6. Geração dos arquivos de saída
        pasta_saida = _obter_pasta_saida()
        caminho_inj = gerar_arquivo_injecao(df_gpon_inj, df_met_inj, pasta_saida)
        caminho_canc = gerar_arquivo_cancelamento(df_excedentes, pasta_saida)

        log.info("Processo finalizado com sucesso!")
        log.info(" - Injeção: %s", caminho_inj)
        log.info(" - Visitas Excedentes: %s", caminho_canc)

    except ValueError as e:
        log.error("Erro de validação de negócio: %s", e)
        sys.exit(1)

    except FileNotFoundError as e:
        log.error("Arquivo não encontrado: %s", e)
        sys.exit(1)

    except Exception as e:
        log.exception("Erro inesperado durante a execução: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()