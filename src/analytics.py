import logging
import pandas as pd

log = logging.getLogger(__name__)


def gerar_resumo(df_injecao: pd.DataFrame, df_cancelamento: pd.DataFrame) -> dict:
    """Imprime e retorna um resumo com a quantidade de ordens por destino.

    Args:
        df_injecao: DataFrame com ordens filtradas para injeção.
        df_cancelamento: DataFrame com ordens filtradas para cancelamento.

    Returns:
        dict com chaves 'injecao', 'cancelamento' e 'total'.
    """
    qtd_injecao = len(df_injecao)
    qtd_cancelamento = len(df_cancelamento)
    total = qtd_injecao + qtd_cancelamento

    separador = "=" * 40
    log.info(separador)
    log.info("         RESUMO ANALÍTICO")
    log.info(separador)
    log.info("  Ordens para INJEÇÃO:      %d", qtd_injecao)
    log.info("  Ordens para CANCELAMENTO: %d", qtd_cancelamento)
    log.info("  TOTAL:                    %d", total)
    log.info(separador)

    return {
        "injecao": qtd_injecao,
        "cancelamento": qtd_cancelamento,
        "total": total,
    }