import os
import logging
import pandas as pd
from datetime import date, timedelta

import config

log = logging.getLogger(__name__)


def _proximas_datas_uteis(quantidade: int, a_partir_de: date = None) -> list[date]:
    """Calcula as próximas N datas úteis (excluindo sábado e domingo).

    Args:
        quantidade: Número de datas úteis desejadas.
        a_partir_de: Data de referência (padrão: amanhã).

    Returns:
        Lista de objetos date com as datas úteis.
    """
    if a_partir_de is None:
        a_partir_de = date.today() + timedelta(days=1)

    datas = []
    dia_atual = a_partir_de

    while len(datas) < quantidade:
        # weekday(): 0=segunda ... 4=sexta, 5=sábado, 6=domingo
        if dia_atual.weekday() < 5:
            datas.append(dia_atual)
        dia_atual += timedelta(days=1)

    return datas


def _distribuir_blocos(total_ordens: int) -> list[tuple[date, str]]:
    """Cria a distribuição equilibrada de (data, slot) via round-robin.

    Gera config.NUM_DATAS_UTEIS × len(config.SLOTS) blocos.
    As ordens são atribuídas ciclicamente entre os blocos.

    Args:
        total_ordens: Quantidade total de ordens a distribuir.

    Returns:
        Lista de tuplas (date, slot_str), uma por ordem.
    """
    datas = _proximas_datas_uteis(config.NUM_DATAS_UTEIS)

    blocos = []
    for slot in config.SLOTS:
        for dt in datas:
            blocos.append((dt, slot))

    distribuicao = [blocos[i % len(blocos)] for i in range(total_ordens)]
    return distribuicao


def gerar_arquivo_injecao(df: pd.DataFrame, pasta_saida: str) -> str:
    """Gera o arquivo INJECAO.xlsx com as colunas de injeção de agenda.

    Colunas geradas:
        - ID_ORDEM: herda da coluna config.COL_ORDEM.
        - NOTDONE: vazio (necessário para automação).
        - TP_ORDEM: herda de config.COL_ATIVIDADE, aplicando config.SUBSTITUICAO_TP_ORDEM.
        - DT_AGENDA: próximas datas úteis, distribuídas equilibradamente.
        - SLOT: turnos distribuídos equilibradamente.

    Args:
        df: DataFrame filtrado com ordens para injeção.
        pasta_saida: Caminho da pasta onde o arquivo será salvo.

    Returns:
        Caminho completo do arquivo gerado.
    """
    total = len(df)
    distribuicao = _distribuir_blocos(total)

    tp_ordem = (
        df[config.COL_ATIVIDADE]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace(config.SUBSTITUICAO_TP_ORDEM)
    )

    df_saida = pd.DataFrame({
        "ID_ORDEM": df[config.COL_ORDEM].values,
        "NOTDONE":  "",
        "TP_ORDEM": tp_ordem.values,
        "DT_AGENDA": [d[0].strftime("%d/%m/%Y") for d in distribuicao],
        "SLOT":      [d[1] for d in distribuicao],
    })

    caminho = os.path.join(pasta_saida, "INJECAO.xlsx")
    df_saida.to_excel(caminho, sheet_name="INJECAO", index=False)

    log.info("Arquivo de injeção gerado: %s (%d ordens)", caminho, total)
    return caminho


def gerar_arquivo_cancelamento(df: pd.DataFrame, pasta_saida: str) -> str:
    """Gera o arquivo CANCELAMENTO.xlsx apenas com a coluna ORDEM.

    Args:
        df: DataFrame filtrado com ordens para cancelamento.
        pasta_saida: Caminho da pasta onde o arquivo será salvo.

    Returns:
        Caminho completo do arquivo gerado.
    """
    df_saida = df[[config.COL_ORDEM]].copy()

    caminho = os.path.join(pasta_saida, "CANCELAMENTO.xlsx")
    df_saida.to_excel(caminho, sheet_name="CANCELAMENTO", index=False)

    log.info("Arquivo de cancelamento gerado: %s (%d ordens)", caminho, len(df_saida))
    return caminho


def gerar_arquivo_cancelamento_gpon(df: pd.DataFrame, pasta_saida: str) -> str:
    """Gera o arquivo CANCELAMENTO_GPON.xlsx com colunas ORDEM e AGING_STTS.

    Args:
        df: DataFrame filtrado com ordens GPON para cancelamento
            (QTD_VISITA >= config.LIMITE_CANCELAMENTO_GPON).
        pasta_saida: Caminho da pasta onde o arquivo será salvo.

    Returns:
        Caminho completo do arquivo gerado.
    """
    caminho = os.path.join(pasta_saida, "CANCELAMENTO_GPON.xlsx")
    df.to_excel(caminho, sheet_name="CANCELAMENTO_GPON", index=False)

    log.info("Arquivo CANCELAMENTO_GPON gerado: %s (%d ordens)", caminho, len(df))
    return caminho