#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para iniciar o jogo de Xadrez contra IA com diferentes dificuldades

Uso:
    python play_chess.py [dificuldade] [cor]
    
Exemplos:
    python play_chess.py easy white      # IA Fácil, você joga com peças brancas
    python play_chess.py medium black    # IA Médio, você joga com peças pretas
    python play_chess.py hard white      # IA Difícil, você joga com peças brancas
"""

import sys
from chess_new import main, Color

def print_help():
    print(__doc__)
    print("Dificuldades disponíveis: easy, medium, hard")
    print("Cores disponíveis: white, black")

if __name__ == '__main__':
    difficulty = 'medium'
    player_color = 'white'
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['easy', 'medium', 'hard']:
            difficulty = sys.argv[1].lower()
        elif sys.argv[1].lower() in ['-h', '--help', 'help']:
            print_help()
            sys.exit(0)
        else:
            print(f"Dificuldade inválida: {sys.argv[1]}")
            print_help()
            sys.exit(1)
    
    if len(sys.argv) > 2:
        if sys.argv[2].lower() in ['white', 'black']:
            player_color = sys.argv[2].lower()
        else:
            print(f"Cor inválida: {sys.argv[2]}")
            print_help()
            sys.exit(1)
    
    print(f"\n🎮 Iniciando Xadrez vs IA")
    print(f"   Dificuldade: {difficulty.upper()}")
    print(f"   Sua cor: {'♔ DOURADA' if player_color == 'white' else '♚ PRETA'}")
    print(f"\nControles:")
    print(f"   - Clique para selecionar e mover peças")
    print(f"   - ESC para sair")
    print(f"   - N para novo jogo")
    print(f"   - U para desfazer")
    print()
    
    main(difficulty=difficulty, player_color=player_color)
