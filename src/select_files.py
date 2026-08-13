
import tkinter as tk

from tkinter import filedialog


def selecionar_arquivo():
    """Essa função abre janelas do explorador de arquivos e permite a seleção das bases.

    Returns:
        tuple: Retorna (caminho_principal, caminho_automidia) ou (None, None) se cancelado.
    """
    root = tk.Tk()
    root.withdraw()
    # Força a janela do explorador a abrir sempre à frente de outros programas
    root.attributes('-topmost', True)

    caminho_principal = filedialog.askopenfilename(
        title="Selecione o arquivo do backlog",
        filetypes=[
            ("Arquivos Excel", "*.xlsx *.xls *.xlsb"),
            ("Todos os arquivos", "*.*")
        ]
    )

    # Se o usuário cancelar a primeira janela, aborta imediatamente
    if not caminho_principal:
        root.destroy()
        return None, None
    else:
        print("Arquivo lido com sucesso")
    
    return caminho_principal

selecionar_arquivo()
