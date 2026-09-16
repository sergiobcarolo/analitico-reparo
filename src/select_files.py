import os
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

log = logging.getLogger(__name__)

# ─── Cores do tema Vivo ──────────────────────────────────────────────────────
_ROXO_VIVO    = "#660099"
_ROXO_HOVER   = "#7A1FB5"
_BRANCO       = "#FFFFFF"
_CINZA_CLARO  = "#F0E6F6"
_VERDE_BOTAO  = "#008542"
_VERDE_HOVER  = "#00A854"



def selecionar_arquivos_entrada() -> dict[str, str] | None:
    """Abre janela temática Vivo para seleção conjunta dos arquivos GPON e METÁLICO.

    Returns:
        dict com chaves 'gpon' e 'metalico' contendo os caminhos absolutos,
        ou None se o usuário fechar a janela sem concluir a seleção.
    """
    selecionados = {"gpon": None, "metalico": None}
    resultado = {"confirmado": False}

    root = tk.Tk()
    root.title("Analítico Reparo — Seleção de Arquivos")
    root.configure(bg=_ROXO_VIVO)
    root.resizable(False, False)

    # ── Centralizar janela na tela ──
    largura, altura = 520, 420
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
    ).pack(pady=(25, 4))

    tk.Label(
        root,
        text="Selecione as bases GPON e METÁLICO para processamento:",
        font=("Segoe UI", 10),
        fg=_CINZA_CLARO,
        bg=_ROXO_VIVO,
    ).pack(pady=(0, 20))

    # ── Seção GPON ──
    frame_gpon = tk.Frame(root, bg=_ROXO_VIVO)
    frame_gpon.pack(fill="x", padx=40, pady=5)

    lbl_gpon = tk.Label(
        frame_gpon,
        text="GPON: Nenhum arquivo selecionado",
        font=("Segoe UI", 9, "italic"),
        fg=_CINZA_CLARO,
        bg=_ROXO_VIVO,
        anchor="w",
    )

    def _escolher_gpon():
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo GPON",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls *.xlsb"), ("Todos os arquivos", "*.*")],
            parent=root,
        )
        if caminho:
            selecionados["gpon"] = caminho
            nome = os.path.basename(caminho)
            lbl_gpon.config(text=f"GPON: {nome}", font=("Segoe UI", 9, "bold"), fg=_BRANCO)

    btn_gpon = tk.Button(
        frame_gpon,
        text="Selecionar GPON",
        font=("Segoe UI", 10, "bold"),
        fg=_ROXO_VIVO,
        bg=_BRANCO,
        activebackground=_ROXO_HOVER,
        activeforeground=_BRANCO,
        relief="flat",
        cursor="hand2",
        width=18,
        command=_escolher_gpon,
    )
    btn_gpon.pack(side="left")
    lbl_gpon.pack(side="left", padx=10)

    # ── Seção METÁLICO ──
    frame_metalico = tk.Frame(root, bg=_ROXO_VIVO)
    frame_metalico.pack(fill="x", padx=40, pady=15)

    lbl_metalico = tk.Label(
        frame_metalico,
        text="METÁLICO: Nenhum arquivo selecionado",
        font=("Segoe UI", 9, "italic"),
        fg=_CINZA_CLARO,
        bg=_ROXO_VIVO,
        anchor="w",
    )

    def _escolher_metalico():
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo METÁLICO",
            filetypes=[("Arquivos Excel", "*.xlsx *.xls *.xlsb"), ("Todos os arquivos", "*.*")],
            parent=root,
        )
        if caminho:
            selecionados["metalico"] = caminho
            nome = os.path.basename(caminho)
            lbl_metalico.config(text=f"METÁLICO: {nome}", font=("Segoe UI", 9, "bold"), fg=_BRANCO)

    btn_metalico = tk.Button(
        frame_metalico,
        text="Selecionar METÁLICO",
        font=("Segoe UI", 10, "bold"),
        fg=_ROXO_VIVO,
        bg=_BRANCO,
        activebackground=_ROXO_HOVER,
        activeforeground=_BRANCO,
        relief="flat",
        cursor="hand2",
        width=18,
        command=_escolher_metalico,
    )
    btn_metalico.pack(side="left")
    lbl_metalico.pack(side="left", padx=10)

    # ── Botão Confirmar/Processar ──
    def _confirmar():
        if not selecionados["gpon"] or not selecionados["metalico"]:
            messagebox.showwarning(
                "Arquivos Obrigatórios",
                "Por favor, selecione ambos os arquivos (GPON e METÁLICO) antes de prosseguir.",
                parent=root,
            )
            return
        resultado["confirmado"] = True
        root.destroy()

    btn_processar = tk.Button(
        root,
        text="PROCESSAR ARQUIVOS",
        font=("Segoe UI", 12, "bold"),
        fg=_BRANCO,
        bg=_VERDE_BOTAO,
        activebackground=_VERDE_HOVER,
        activeforeground=_BRANCO,
        relief="flat",
        cursor="hand2",
        width=24,
        height=2,
        command=_confirmar,
    )
    btn_processar.pack(pady=(35, 10))

    root.mainloop()

    if resultado["confirmado"]:
        log.info("Arquivos selecionados: GPON=%s | METÁLICO=%s", selecionados["gpon"], selecionados["metalico"])
        return selecionados

    return None


