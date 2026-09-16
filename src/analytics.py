import logging
import pandas as pd

log = logging.getLogger(__name__)


def gerar_resumo_consolidado(
    df_gpon_inj: pd.DataFrame,
    df_met_inj: pd.DataFrame,
    df_excedentes: pd.DataFrame,
) -> dict:
    """Imprime e retorna o painel analítico consolidado da automação.

    Args:
        df_gpon_inj: DataFrame com ordens GPON para injeção.
        df_met_inj: DataFrame com ordens METÁLICO para injeção.
        df_excedentes: DataFrame unificado com ordens de >= 4 visitas.

    Returns:
        dict com as métricas quantitativas do processamento.
    """
    import config

    total_gpon_inj = len(df_gpon_inj)
    total_met_inj  = len(df_met_inj)
    total_injecao  = total_gpon_inj + total_met_inj

    # Contagem de excedentes por classificação
    qtd_gpon_exc = 0
    qtd_met_exc  = 0
    if not df_excedentes.empty and config.COL_CLASSIFICACAO in df_excedentes.columns:
        classificacoes = df_excedentes[config.COL_CLASSIFICACAO].astype(str).str.upper().str.strip()
        qtd_gpon_exc = int((classificacoes == config.VALOR_CLASSIFICACAO_GPON).sum())
        qtd_met_exc  = int((classificacoes == config.VALOR_CLASSIFICACAO_MET).sum())

    total_excedentes = len(df_excedentes)
    total_geral      = total_injecao + total_excedentes

    separador = "=" * 55
    log.info(separador)
    log.info("           RESUMO ANALÍTICO CONSOLIDADO")
    log.info(separador)
    log.info("  ORDENS PARA INJEÇÃO:")
    log.info("    - GPON:                             %d", total_gpon_inj)
    log.info("    - METÁLICO:                         %d", total_met_inj)
    log.info("    * Subtotal Injeção:                 %d", total_injecao)
    log.info("  -----------------------------------------------------")
    log.info("  ORDENS COM VISITAS >= 4 (CANCELAMENTO):")
    log.info("    - GPON:                             %d", qtd_gpon_exc)
    log.info("    - METÁLICO:                         %d", qtd_met_exc)
    log.info("    * Subtotal Cancelamento:            %d", total_excedentes)
    log.info("  =====================================================")
    log.info("  TOTAL DE ORDENS PROCESSADAS:          %d", total_geral)
    log.info(separador)

    return {
        "gpon_injecao": total_gpon_inj,
        "metalico_injecao": total_met_inj,
        "total_injecao": total_injecao,
        "gpon_excedentes": qtd_gpon_exc,
        "metalico_excedentes": qtd_met_exc,
        "total_excedentes": total_excedentes,
        "total_geral": total_geral,
    }