@echo off
REM Script para fazer push para GitHub
REM Cole seu token GitHub PAT quando solicitado

echo Digite seu token GitHub PAT (Personal Access Token):
set /p TOKEN=

cd /d %~dp0

REM Temporariamente configurar URL com token
git remote set-url origin https://wzinn1314:%TOKEN%@github.com/wzinn1314/xadrez.git

REM Fazer push
git push -u origin main

REM Remover token da configuração
git remote set-url origin https://github.com/wzinn1314/xadrez.git

echo Push concluído!
pause
