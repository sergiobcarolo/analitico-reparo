import logging
import tkinter as tk
from tkinter import filedialog

log = logging.getLogger(__name__)

# ─── Cores do tema Vivo ──────────────────────────────────────────────────────
_ROXO_VIVO   = "#660099"
_ROXO_HOVER  = "#7A1FB5"
_BRANCO      = "#FFFFFF"
_CINZA_CLARO = "#F0E6F6"


def selecionar_caminho() -> str | None:
    """Abre janela temática Vivo para escolher o caminho de análise.

    Returns:
        'metalico' | 'gpon' | None (se a janela for fechada sem escolha).
    """
    escolha = {"valor": None}

    root = tk.Tk()
    root.title("Analítico Reparo — Vivo")
    root.configure(bg=_ROXO_VIVO)
    root.resizable(False, False)

    # ── Centralizar janela na tela ──
    largura, altura = 420, 320
    x = (root.winfo_screenwidth() - largura) // 2
    y = (root.winfo_screenheight() - altura) // 2
    root.geometry(f"{largura}x{altura}+{x}+{y}")
    root.attributes("-topmost", True)

    # ── Título ──
    tk.Label(
        root,
        text="ANALÍTICO REPARO",
        font=("Segoe UI", 18, "bold"),
        fg=_BRANCO,
        bg=_ROXO_VIVO,
    ).pack(pady=(30, 5))

    tk.Label(
        root,
        text="Selecione o tipo de análise:",
        font=("Segoe UI", 11),
        fg=_CINZA_CLARO,
        bg=_ROXO_VIVO,
    ).pack(pady=(0, 25))

    # ── Helpers para hover ──
    def _on_enter(e):
        e.widget.config(bg=_ROXO_VIVO, fg=_BRANCO)

    def _on_leave(e):
        e.widget.config(bg=_BRANCO, fg=_ROXO_VIVO)

    def _criar_botao(texto, valor):
        btn = tk.Button(
            root,
            text=texto,
            font=("Segoe UI", 13, "bold"),
            fg=_ROXO_VIVO,
            bg=_BRANCO,
            activebackground=_ROXO_HOVER,
            activeforeground=_BRANCO,
            relief="flat",
            cursor="hand2",
            width=22,
            height=2,
            command=lambda: (_set(valor)),
        )
        btn.pack(pady=8)
        btn.bind("<Enter>", _on_enter)
        btn.bind("<Leave>", _on_leave)
        return btn

    def _set(valor):
        escolha["valor"] = valor
        root.destroy()

    _criar_botao("METÁLICO SIEBEL", "metalico")
    _criar_botao("GPON", "gpon")

    root.mainloop()

    if escolha["valor"]:
        log.info("Caminho selecionado: %s", escolha["valor"])
    return escolha["valor"]


def selecionar_arquivo():
    """Abre janela do explorador de arquivos para seleção do backlog.

    Returns:
        str | None: Caminho do arquivo selecionado ou None se cancelado.
    """
    root = tk.Tk()
    root.withdraw()
    # Força a janela do explorador a abrir sempre à frente de outros programas
    root.attributes('-topmost', True)

    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo do backlog",
        filetypes=[
            ("Arquivos Excel", "*.xlsx *.xls *.xlsb"),
            ("Todos os arquivos", "*.*")
        ]
    )

    root.destroy()

    if not caminho:
        return None

    log.info("Arquivo selecionado: %s", caminho)
    return caminho

