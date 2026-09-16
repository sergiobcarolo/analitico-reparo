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


def _distribuir_blocos_metalico(total_ordens: int) -> list[tuple[date, str]]:
    """Cria a distribuição equilibrada de (data, slot) para ordens METÁLICO via round-robin.

    Regra METÁLICO:
        - 3 dias úteis subsequentes (excluindo sábados e domingos).
        - Intercalados entre os slots da manhã e da tarde.

    Args:
        total_ordens: Quantidade total de ordens METÁLICO a distribuir.

    Returns:
        Lista de tuplas (date, slot_str), uma por ordem.
    """
    if total_ordens == 0:
        return []

    datas = _proximas_datas_uteis(config.NUM_DATAS_UTEIS)

    blocos = []
    for slot in config.SLOTS:
        for dt in datas:
            blocos.append((dt, slot))

    distribuicao = [blocos[i % len(blocos)] for i in range(total_ordens)]
    return distribuicao


def _distribuir_blocos_gpon(total_ordens: int) -> list[tuple[date, str]]:
    """Cria a distribuição de (data, slot) para ordens GPON conforme plano de negócio.

    Regra GPON:
        - 30% das ordens para HOJE no slot da TARDE (12:30-18:00).
        - 70% das ordens para o DIA SEGUINTE divididas entre MANHÃ (08:30-12:30) e TARDE (12:30-18:00).
        - Dias posteriores são corridos (sem se preocupar com feriados ou finais de semana).

    Args:
        total_ordens: Quantidade total de ordens GPON a distribuir.

    Returns:
        Lista de tuplas (date, slot_str), uma por ordem.
    """
    if total_ordens == 0:
        return []

    hoje = date.today()
    dia_seguinte = hoje + timedelta(days=1)

    qtd_hoje = round(total_ordens * config.PERCENTUAL_GPON_HOJE)
    qtd_amanha = total_ordens - qtd_hoje

    distribuicao: list[tuple[date, str]] = []

    # 30% hoje no slot da tarde
    for _ in range(qtd_hoje):
        distribuicao.append((hoje, config.SLOT_TARDE))

    # 70% dia seguinte divididos entre manhã e tarde (round-robin)
    slots_amanha = [config.SLOT_MANHA, config.SLOT_TARDE]
    for i in range(qtd_amanha):
        distribuicao.append((dia_seguinte, slots_amanha[i % 2]))

    return distribuicao


def _formatar_para_injecao(df: pd.DataFrame, distribuicao: list[tuple[date, str]]) -> pd.DataFrame:
    """Formata um DataFrame de ordens válidas para o padrão de colunas do INJECAO.xlsx.

    Colunas geradas:
        - ID_ORDEM: coluna config.COL_ORDEM.
        - NOTDONE: string vazia.
        - TP_ORDEM: config.COL_ATIVIDADE aplicando substituições definidas em config.
        - DT_AGENDA: data formatada (DD/MM/AAAA).
        - SLOT: slot de horário atribuído.

    Args:
        df: DataFrame de entrada.
        distribuicao: Lista de tuplas (data, slot) correspondentes.

    Returns:
        DataFrame formatado com o leiaute final de injeção.
    """
    if df.empty:
        return pd.DataFrame(columns=["ID_ORDEM", "NOTDONE", "TP_ORDEM", "DT_AGENDA", "SLOT"])

    tp_ordem = (
        df[config.COL_ATIVIDADE]
        .astype(str)
        .str.strip()
        .str.upper()
        .replace(config.SUBSTITUICAO_TP_ORDEM)
    )

    return pd.DataFrame({
        "ID_ORDEM":  df[config.COL_ORDEM].values,
        "NOTDONE":   "",
        "TP_ORDEM":  tp_ordem.values,
        "DT_AGENDA": [d[0].strftime("%d/%m/%Y") for d in distribuicao],
        "SLOT":      [d[1] for d in distribuicao],
    })


def gerar_arquivo_injecao(
    df_gpon: pd.DataFrame, df_metalico: pd.DataFrame, pasta_saida: str
) -> str:
    """Gera o arquivo unificado INJECAO.xlsx com priorização estrita de ordens.

    Ordem de gravação no arquivo (prioridade de injeção):
        1º: Ordens GPON para o mesmo dia à tarde (12:30-18:00).
        2º: Ordens GPON para o dia seguinte (manhã/tarde).
        3º: Ordens METÁLICO (3 dias úteis subsequentes intercalados).

    Args:
        df_gpon: DataFrame com ordens GPON válidas para injeção (já ordenadas por prioridade).
        df_metalico: DataFrame com ordens METÁLICO válidas para injeção.
        pasta_saida: Caminho da pasta de destino.

    Returns:
        Caminho absoluto do arquivo INJECAO.xlsx gerado.
    """
    # 1º e 2º: Distribuição e formatação GPON (Hoje tarde primeiro, depois amanhã)
    dist_gpon = _distribuir_blocos_gpon(len(df_gpon))
    df_gpon_formatado = _formatar_para_injecao(df_gpon, dist_gpon)

    # 3º: Distribuição e formatação METÁLICO (por último)
    dist_met = _distribuir_blocos_metalico(len(df_metalico))
    df_met_formatado = _formatar_para_injecao(df_metalico, dist_met)

    # Unifica preservando a ordem: GPON (Hoje tarde -> Outro dia) seguido de METÁLICO
    df_injecao_total = pd.concat([df_gpon_formatado, df_met_formatado], ignore_index=True)

    caminho = os.path.join(pasta_saida, config.ARQUIVO_INJECAO)
    df_injecao_total.to_excel(caminho, sheet_name=config.ABA_INJECAO, index=False)

    log.info(
        "Arquivo de injeção gerado: %s (Total: %d ordens | 1º GPON Hoje/Amanhã: %d, 2º METÁLICO: %d)",
        caminho,
        len(df_injecao_total),
        len(df_gpon_formatado),
        len(df_met_formatado),
    )
    return caminho


def gerar_arquivo_cancelamento(df_excedentes: pd.DataFrame, pasta_saida: str) -> str:
    """Gera o arquivo unificado CANCELAMENTO.xlsx com ordens com QTD_VISITA >= 4.

    Args:
        df_excedentes: DataFrame unificado contendo ordens GPON e METÁLICO com >= 4 visitas.
        pasta_saida: Caminho da pasta de destino.

    Returns:
        Caminho absoluto do arquivo gerado.
    """
    colunas_saida = [config.COL_ORDEM, config.COL_CLASSIFICACAO]
    if config.COL_QTD_VISITA in df_excedentes.columns:
        colunas_saida.append(config.COL_QTD_VISITA)

    df_saida = df_excedentes[colunas_saida].copy()

    caminho = os.path.join(pasta_saida, config.ARQUIVO_CANCELAMENTO)
    df_saida.to_excel(caminho, sheet_name=config.ABA_CANCELAMENTO, index=False)

    log.info(
        "Arquivo de visitas excedentes (%s) gerado: %s (%d ordens)",
        config.ARQUIVO_CANCELAMENTO,
        caminho,
        len(df_saida),
    )
    return caminho