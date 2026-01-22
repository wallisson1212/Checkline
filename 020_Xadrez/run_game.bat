@echo off
REM run_game.bat - Cria/ativa venv, instala pygame e roda chess.py
REM Execute no CMD ou dando duplo clique na pasta do projeto.

cd /d %~dp0

IF NOT EXIST ".venv\Scripts\activate.bat" (
  echo Criando virtualenv .venv...
  python -m venv .venv
)

echo Ativando .venv...
call .venv\Scripts\activate.bat

echo Atualizando pip e instalando pygame...
python -m pip install --upgrade pip
python -m pip install pygame

echo Iniciando chess.py...
python ..\Xadrez\chess.py
pause