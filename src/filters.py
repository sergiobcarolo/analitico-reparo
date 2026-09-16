import logging
import pandas as pd

import config

log = logging.getLogger(__name__)


def filtrar_gpon_injecao(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra ordens GPON elegíveis para injeção e remove duplicatas.

    Critérios:
        - CLASSIFICACAO == 'GPON'
        - SISTEMA == 'SIEBEL'
        - AGING_STTS >= 1
        - QTD_VISITA <= 3

    Args:
        df: DataFrame bruto do arquivo GPON.

    Returns:
        DataFrame com ordens GPON válidas para injeção.
    """
    df_copia = df.copy()
    aging = pd.to_numeric(df_copia[config.COL_AGING_STTS], errors="coerce").fillna(0)
    visitas = pd.to_numeric(df_copia[config.COL_QTD_VISITA], errors="coerce").fillna(999)

    mascara = (
        (df_copia[config.COL_CLASSIFICACAO].astype(str).str.upper().str.strip() == config.VALOR_CLASSIFICACAO_GPON)
        & (df_copia[config.COL_SISTEMA].astype(str).str.upper().str.strip() == config.VALOR_SISTEMA)
        & (aging >= 1)
        & (visitas <= config.LIMITE_INJECAO)
    )

    df_filtrado = df_copia[mascara].copy()
    antes = len(df_filtrado)
    df_filtrado = df_filtrado.drop_duplicates()
    duplicatas = antes - len(df_filtrado)

    # Ordena por AGING_STTS decrescente para priorizar ordens com maior tempo de espera
    df_filtrado = df_filtrado.sort_values(by=config.COL_AGING_STTS, ascending=False).reset_index(drop=True)

    log.info("GPON válidas para injeção: %d (removidas %d duplicatas)", len(df_filtrado), duplicatas)
    return df_filtrado


def filtrar_metalico_injecao(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra ordens METÁLICO elegíveis para injeção e remove duplicatas.

    Critérios:
        - CLASSIFICACAO == 'METALICO'
        - SISTEMA == 'SIEBEL'
        - QTD_VISITA <= 3

    Args:
        df: DataFrame bruto do arquivo METÁLICO.

    Returns:
        DataFrame com ordens METÁLICO válidas para injeção.
    """
    df_copia = df.copy()
    visitas = pd.to_numeric(df_copia[config.COL_QTD_VISITA], errors="coerce").fillna(999)

    mascara = (
        (df_copia[config.COL_CLASSIFICACAO].astype(str).str.upper().str.strip() == config.VALOR_CLASSIFICACAO_MET)
        & (df_copia[config.COL_SISTEMA].astype(str).str.upper().str.strip() == config.VALOR_SISTEMA)
        & (visitas <= config.LIMITE_INJECAO)
    )

    df_filtrado = df_copia[mascara].copy()
    antes = len(df_filtrado)
    df_filtrado = df_filtrado.drop_duplicates()
    duplicatas = antes - len(df_filtrado)

    log.info("METÁLICO válidas para injeção: %d (removidas %d duplicatas)", len(df_filtrado), duplicatas)
    return df_filtrado


def filtrar_ordens_excedentes(df_gpon: pd.DataFrame, df_metalico: pd.DataFrame) -> pd.DataFrame:
    """Filtra ordens com QTD_VISITA >= 4 de ambos os arquivos e unifica o resultado.

    Args:
        df_gpon: DataFrame com dados do GPON.
        df_metalico: DataFrame com dados do METÁLICO.

    Returns:
        DataFrame consolidado com colunas ORDEM, CLASSIFICACAO e QTD_VISITA, sem duplicatas.
    """
    colunas_saida = [config.COL_ORDEM, config.COL_CLASSIFICACAO, config.COL_QTD_VISITA]

    # GPON com visitas >= 4
    df_g = df_gpon.copy()
    visitas_g = pd.to_numeric(df_g[config.COL_QTD_VISITA], errors="coerce").fillna(0)
    mascara_g = (
        (df_g[config.COL_CLASSIFICACAO].astype(str).str.upper().str.strip() == config.VALOR_CLASSIFICACAO_GPON)
        & (df_g[config.COL_SISTEMA].astype(str).str.upper().str.strip() == config.VALOR_SISTEMA)
        & (visitas_g >= config.LIMITE_CANCELAMENTO)
    )
    df_g_exc = df_g[mascara_g][colunas_saida].copy()

    # METÁLICO com visitas >= 4
    df_m = df_metalico.copy()
    visitas_m = pd.to_numeric(df_m[config.COL_QTD_VISITA], errors="coerce").fillna(0)
    mascara_m = (
        (df_m[config.COL_CLASSIFICACAO].astype(str).str.upper().str.strip() == config.VALOR_CLASSIFICACAO_MET)
        & (df_m[config.COL_SISTEMA].astype(str).str.upper().str.strip() == config.VALOR_SISTEMA)
        & (visitas_m >= config.LIMITE_CANCELAMENTO)
    )
    df_m_exc = df_m[mascara_m][colunas_saida].copy()

    unificado = pd.concat([df_g_exc, df_m_exc], ignore_index=True)
    antes = len(unificado)
    unificado = unificado.drop_duplicates()
    duplicatas = antes - len(unificado)

    log.info(
        "Ordens unificadas com QTD_VISITA >= %d: %d (GPON: %d, MET: %d, duplicatas removidas: %d)",
        config.LIMITE_CANCELAMENTO,
        len(unificado),
        len(df_g_exc),
        len(df_m_exc),
        duplicatas,
    )
    return unificado