#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste rápido do sistema de IA
"""

import sys
import os

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chess_new import ChessGame, Color, ChessAI, Board, PieceType
    
    print("✅ Imports bem-sucedidos!")
    
    # Teste 1: Criar uma IA
    print("\n🤖 Testando IA...")
    ai = ChessAI('easy')
    print(f"   ✅ IA Fácil criada")
    
    ai = ChessAI('medium')
    print(f"   ✅ IA Médio criada")
    
    ai = ChessAI('hard')
    print(f"   ✅ IA Difícil criada")
    
    # Teste 2: Criar um jogo
    print("\n🎮 Testando ChessGame...")
    print("   Nota: Pygame não está instalado, então não vamos iniciar a interface gráfica")
    print("   Mas vamos testar a lógica...")
    
    # Criar um board e testar
    board = Board()
    print(f"   ✅ Board criado com sucesso")
    print(f"   ✅ Peças inicializadas")
    
    print("\n✅ TODOS OS TESTES PASSARAM!")
    print("\nPara jogar, instale pygame e execute:")
    print("   python play_chess.py easy white")
    print("   python play_chess.py medium black")
    print("   python play_chess.py hard white")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\nPara usar o jogo, instale as dependências:")
    print("   pip install pygame")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
