@echo off
title INJECAO REPARO

cd /d "%~dp0"

echo ========================================
echo  Injecao-Reparo
echo ========================================
echo.

:: Cria venv se não existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativa venv
call venv\Scripts\activate

:: Instala dependências
echo Instalando dependencias...
pip install -r requirements.txt -qq
echo Dependencias prontas!

echo.
echo ========================================
echo  Iniciando automacao
echo ========================================
echo.

python main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] A automacao finalizou com codigo de erro: %ERRORLEVEL%
) else (
    echo.
    echo [OK] Automacao finalizada com sucesso.
)

echo.
pause