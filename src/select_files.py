import logging
import tkinter as tk
from tkinter import filedialog

log = logging.getLogger(__name__)


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
