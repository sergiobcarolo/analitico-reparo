import logging
import pandas as pd

import config

log = logging.getLogger(__name__)


def aplicar_filtro_base(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros obrigatórios e remove duplicatas.

    Filtros:
        - SISTEMA == config.VALOR_SISTEMA
        - CLASSIFICACAO == config.VALOR_CLASSIFICACAO
        - Remoção de linhas inteiramente duplicadas.

    Args:
        df: DataFrame com os dados brutos do backlog.

    Returns:
        DataFrame filtrado e sem duplicatas.
    """
    df_filtrado = df[
        (df[config.COL_SISTEMA].str.upper().str.strip() == config.VALOR_SISTEMA)
        & (df[config.COL_CLASSIFICACAO].str.upper().str.strip() == config.VALOR_CLASSIFICACAO)
    ].copy()

    antes = len(df_filtrado)
    df_filtrado = df_filtrado.drop_duplicates()
    duplicatas = antes - len(df_filtrado)

    log.info("Registros após filtro base: %d (removidas %d duplicatas)", len(df_filtrado), duplicatas)
    return df_filtrado


def filtrar_injecao(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna ordens com QTD_VISITA <= config.LIMITE_INJECAO (candidatas à injeção).

    Args:
        df: DataFrame já com filtro base aplicado.

    Returns:
        DataFrame com ordens para injeção.
    """
    resultado = df[df[config.COL_QTD_VISITA] <= config.LIMITE_INJECAO].copy()
    log.info("Ordens para injeção: %d", len(resultado))
    return resultado


def filtrar_cancelamento(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna ordens com QTD_VISITA > config.LIMITE_INJECAO (candidatas a cancelamento).

    Args:
        df: DataFrame já com filtro base aplicado.

    Returns:
        DataFrame com ordens para cancelamento.
    """
    resultado = df[df[config.COL_QTD_VISITA] > config.LIMITE_INJECAO].copy()
    log.info("Ordens para cancelamento: %d", len(resultado))
    return resultado