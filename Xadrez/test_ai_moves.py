#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Teste da IA para verificar se ela está fazendo movimentos
"""

import sys
import os

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chess_new import ChessGame, ChessAI, Color, Board
    
    print("✅ Imports bem-sucedidos!")
    
    # Teste com a IA em diferentes dificuldades
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n🤖 Testando IA {difficulty.upper()}...")
        
        # Criar um jogo
        game = ChessGame(ai_enabled=True, ai_difficulty=difficulty, player_color=Color.WHITE)
        ai = game.ai
        
        # Testar 5 movimentos da IA
        for move_num in range(5):
            # Simular movimento do jogador (primeiro movimento padrão)
            player_moves = game.get_piece_moves(4, 6)  # Peão branco e4
            if player_moves:
                to_x, to_y = list(player_moves)[0]
                game.make_move(4, 6, to_x, to_y)
                print(f"   Movimento {move_num + 1}: Jogador moveu peça")
            
            # Pedir movimento da IA
            ai_move = ai.get_best_move(game, game.ai_color)
            
            if ai_move:
                from_x, from_y, to_x, to_y = ai_move
                print(f"   Movimento {move_num + 1}: IA tentou mover ({from_x},{from_y}) -> ({to_x},{to_y})")
                
                # Executar movimento
                success = game.make_move(from_x, from_y, to_x, to_y)
                if success:
                    print(f"   ✅ Movimento da IA foi bem-sucedido!")
                else:
                    print(f"   ❌ Movimento da IA falhou!")
                    break
            else:
                print(f"   ❌ IA não conseguiu gerar movimento!")
                break
            
            if game.game_over:
                print(f"   🏁 Jogo terminou!")
                break
        
        print(f"   ✅ Teste de IA {difficulty.upper()} concluído")
    
    print("\n✅ TESTES DE IA CONCLUÍDOS COM SUCESSO!")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
