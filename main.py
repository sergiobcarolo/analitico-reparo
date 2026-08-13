"""Orquestrador principal do Analítico Reparo."""

import os
import sys
import logging
import pandas as pd

# Adiciona o diretório raiz ao path para importar os módulos de src/ e config
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from src.select_files import selecionar_caminho, selecionar_arquivo
from src.filters import (
    aplicar_filtro_base, filtrar_injecao, filtrar_cancelamento,
    aplicar_filtro_base_gpon, filtrar_cancelamento_gpon,
)
from src.analytics import gerar_resumo, gerar_resumo_gpon
from src.generate_files import (
    gerar_arquivo_injecao, gerar_arquivo_cancelamento,
    gerar_arquivo_cancelamento_gpon,
)

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


def _validar_colunas_gpon(df: pd.DataFrame) -> None:
    """Verifica colunas obrigatórias para o fluxo GPON.

    Raises:
        ValueError: Se alguma coluna obrigatória estiver ausente.
    """
    necessarias = [config.COL_CLASSIFICACAO, config.COL_QTD_VISITA,
                   config.COL_ORDEM, config.COL_AGING_STTS]
    faltando = [c for c in necessarias if c not in df.columns]
    if faltando:
        raise ValueError(
            f"Colunas GPON não encontradas: {faltando}\n"
            f"Colunas disponíveis: {list(df.columns)}"
        )


def _obter_pasta_saida() -> str:
    """Cria e retorna o caminho da pasta de saída."""
    pasta = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), config.PASTA_SAIDA
    )
    os.makedirs(pasta, exist_ok=True)
    return pasta


def _fluxo_metalico(df: pd.DataFrame) -> None:
    """Executa o fluxo de análise para ordens METÁLICO SIEBEL."""
    validar_colunas(df)

    df_filtrado     = aplicar_filtro_base(df)
    df_injecao      = filtrar_injecao(df_filtrado)
    df_cancelamento = filtrar_cancelamento(df_filtrado)

    gerar_resumo(df_injecao, df_cancelamento)

    pasta_saida = _obter_pasta_saida()
    gerar_arquivo_injecao(df_injecao, pasta_saida)
    gerar_arquivo_cancelamento(df_cancelamento, pasta_saida)

    log.info("Processo METÁLICO finalizado! Arquivos em: %s", pasta_saida)


def _fluxo_gpon(df: pd.DataFrame) -> None:
    """Executa o fluxo de análise para ordens GPON."""
    _validar_colunas_gpon(df)

    df_gpon = aplicar_filtro_base_gpon(df)

    if df_gpon.empty:
        log.warning("Nenhuma ordem GPON encontrada no arquivo.")
        return

    gerar_arquivo = gerar_resumo_gpon(df_gpon)

    if gerar_arquivo:
        df_cancelamento = filtrar_cancelamento_gpon(df_gpon)

        if df_cancelamento.empty:
            log.warning("Nenhuma ordem GPON com QTD_VISITA >= %d.", config.LIMITE_CANCELAMENTO_GPON)
            return

        pasta_saida = _obter_pasta_saida()
        gerar_arquivo_cancelamento_gpon(df_cancelamento, pasta_saida)
        log.info("Processo GPON finalizado! Arquivo em: %s", pasta_saida)
    else:
        log.info("Geração do arquivo CANCELAMENTO_GPON cancelada pelo usuário.")


def main():
    try:
        # 1. Seleção do caminho (METÁLICO ou GPON)
        caminho_tipo = selecionar_caminho()
        if caminho_tipo is None:
            log.warning("Nenhum caminho selecionado. Encerrando.")
            return

        # 2. Seleção do arquivo
        caminho = selecionar_arquivo()
        if caminho is None:
            log.warning("Nenhum arquivo selecionado. Encerrando.")
            return

        # 3. Leitura do Excel
        log.info("Lendo arquivo...")
        df = pd.read_excel(caminho)
        log.info("Registros lidos: %d", len(df))

        # 4. Direciona para o fluxo correto
        if caminho_tipo == "metalico":
            _fluxo_metalico(df)
        elif caminho_tipo == "gpon":
            _fluxo_gpon(df)

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