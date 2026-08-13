# ─── Nomes das Colunas do Excel de Entrada ────────────────────────────────────
COL_SISTEMA        = "SISTEMA"
COL_CLASSIFICACAO  = "CLASSIFICACAO"
COL_QTD_VISITA     = "QTD_VISITA"
COL_ORDEM          = "ORDEM"
COL_ATIVIDADE      = "ATIVIDADE"

# ─── Valores de Filtro ────────────────────────────────────────────────────────
VALOR_SISTEMA      = "SIEBEL"
VALOR_CLASSIFICACAO = "METALICO"

# ─── Limiar de Injeção ────────────────────────────────────────────────────────
LIMITE_INJECAO     = 3      # QTD_VISITA <= LIMITE_INJECAO → injeção

# ─── GPON ─────────────────────────────────────────────────────────────────────
VALOR_CLASSIFICACAO_GPON = "GPON"
COL_AGING_STTS           = "AGING_STTS"
LIMITE_CANCELAMENTO_GPON = 4   # QTD_VISITA >= 4 → cancelamento GPON

# ─── Slots de Horário ─────────────────────────────────────────────────────────
SLOTS              = ["08:30-12:30", "12:30-18:00"]
NUM_DATAS_UTEIS    = 3

# ─── Substituição de Valor em TP_ORDEM ────────────────────────────────────────
SUBSTITUICAO_TP_ORDEM = {"BD": "REPARO"}

# ─── Pasta de Saída ───────────────────────────────────────────────────────────
PASTA_SAIDA        = "output"

# ─── Colunas Obrigatórias para Validação ──────────────────────────────────────
COLUNAS_OBRIGATORIAS = [
    COL_SISTEMA,
    COL_CLASSIFICACAO,
    COL_QTD_VISITA,
    COL_ORDEM,
    COL_ATIVIDADE,
]
