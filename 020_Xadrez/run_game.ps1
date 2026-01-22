# run_game.ps1 - Cria/ativa venv, instala pygame e roda chess.py
# Execute no PowerShell a partir da pasta do projeto:
#   .\run_game.ps1

$ErrorActionPreference = "Stop"
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

# Se não existir, cria o venv
if (-Not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "Criando virtualenv .venv..." -ForegroundColor Cyan
    python -m venv .venv
}

# Permite execução para esta sessão (não altera política global)
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Ativa o venv
Write-Host "Ativando .venv..." -ForegroundColor Cyan
.\.venv\Scripts\Activate.ps1

# Atualiza pip e instala pygame
Write-Host "Atualizando pip e instalando pygame..." -ForegroundColor Cyan
python -m pip install --upgrade pip
python -m pip install pygame

# Executa o jogo
Write-Host "Iniciando chess.py..." -ForegroundColor Green
python ..\Xadrez\chess.py
