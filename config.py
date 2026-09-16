# ─── Nomes das Colunas do Excel de Entrada ────────────────────────────────────
COL_SISTEMA        = "SISTEMA"
COL_CLASSIFICACAO  = "CLASSIFICACAO"
COL_QTD_VISITA     = "QTD_VISITA"
COL_ORDEM          = "ORDEM"
COL_ATIVIDADE      = "ATIVIDADE"
COL_AGING_STTS     = "AGING_STTS"

# ─── Valores de Filtro ────────────────────────────────────────────────────────
VALOR_SISTEMA            = "SIEBEL"
VALOR_CLASSIFICACAO_MET  = "METALICO"
VALOR_CLASSIFICACAO_GPON = "GPON"

# ─── Limiares de Regra de Negócio ─────────────────────────────────────────────
LIMITE_INJECAO       = 3      # QTD_VISITA <= 3 → injeção
LIMITE_CANCELAMENTO  = 4      # QTD_VISITA >= 4 → arquivo unificado
PERCENTUAL_GPON_HOJE = 0.30   # 30% hoje (tarde), 70% amanhã (dividido manhã/tarde)

# ─── Slots de Horário ─────────────────────────────────────────────────────────
SLOT_MANHA         = "08:30-12:30"
SLOT_TARDE         = "12:30-18:00"
SLOTS              = [SLOT_MANHA, SLOT_TARDE]
NUM_DATAS_UTEIS    = 3        # Metálico: 3 dias úteis

# ─── Substituição de Valor em TP_ORDEM ────────────────────────────────────────
SUBSTITUICAO_TP_ORDEM = {"BD": "REPARO"}

# ─── Arquivos e Pastas de Saída ───────────────────────────────────────────────
PASTA_SAIDA          = "output"
ARQUIVO_INJECAO      = "INJECAO.xlsx"
ABA_INJECAO          = "INJECAO"
ARQUIVO_CANCELAMENTO = "CANCELAMENTO.xlsx"
ABA_CANCELAMENTO     = "CANCELAMENTO"

# ─── Colunas Obrigatórias para Validação ──────────────────────────────────────
COLUNAS_OBRIGATORIAS_METALICO = [
    COL_SISTEMA,
    COL_CLASSIFICACAO,
    COL_QTD_VISITA,
    COL_ORDEM,
    COL_ATIVIDADE,
]

COLUNAS_OBRIGATORIAS_GPON = [
    COL_SISTEMA,
    COL_CLASSIFICACAO,
    COL_QTD_VISITA,
    COL_ORDEM,
    COL_ATIVIDADE,
    COL_AGING_STTS,
]

