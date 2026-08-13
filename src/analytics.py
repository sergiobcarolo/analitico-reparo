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


def gerar_resumo_gpon(df: pd.DataFrame) -> bool:
    """Exibe tabela cruzada AGING_STTS × QTD_VISITA e pergunta se deseja gerar arquivo.

    A tabela mostra a quantidade de ordens para cada combinação de
    AGING_STTS (linhas) e QTD_VISITA (colunas), permitindo identificar
    ordens com aging alto e sem visitas, por exemplo.

    Args:
        df: DataFrame GPON já com filtro base aplicado.

    Returns:
        True se o usuário deseja gerar o arquivo CANCELAMENTO_GPON, False caso contrário.
    """
    import config

    tabela = pd.crosstab(
        df[config.COL_AGING_STTS],
        df[config.COL_QTD_VISITA],
        margins=True,
        margins_name="TOTAL",
    )

    separador = "=" * 60
    log.info(separador)
    log.info("    ANALÍTICO GPON — AGING_STTS × QTD_VISITA")
    log.info(separador)
    print()
    print(tabela.to_string())
    print()
    log.info(separador)
    log.info("  Total de ordens GPON: %d", len(df))
    log.info(separador)

    resposta = input("\nDeseja gerar o arquivo CANCELAMENTO_GPON? (s/n): ").strip().lower()
    return resposta in ("s", "sim", "y", "yes")