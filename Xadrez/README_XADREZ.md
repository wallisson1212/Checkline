# ♔ XADREZZZ - Jogo de Xadrez vs IA ♚

Um jogo de xadrez completo com inteligência artificial em 3 níveis de dificuldade.

## 🎮 Como Jogar

### Instalação das Dependências

```bash
pip install pygame
```

### Iniciando o Jogo

```bash
# IA Fácil, você com peças brancas (douradas)
python play_chess.py easy white

# IA Médio, você com peças pretas
python play_chess.py medium black

# IA Difícil, você com peças brancas
python play_chess.py hard white
```

### Padrão
Se não especificar nada:
```bash
python play_chess.py
# Será: dificuldade=medium, cor=white
```

## ⌨️ Controles

- **Clique do Mouse**: Selecionar uma peça e depois clicar onde deseja mover
- **ESC**: Sair do jogo
- **N**: Começar um novo jogo
- **U**: Desfazer o último movimento

## 🤖 Níveis de Dificuldade

### 🟢 Fácil (Easy)
- A IA faz movimentos completamente aleatórios
- Ideal para iniciantes
- Sem análise estratégica

### 🟡 Médio (Medium)
- A IA usa algoritmo Minimax com profundidade 3
- Avalia posições do tabuleiro
- Considera valor das peças e posicionamento
- Bom desafio para jogadores intermediários

### 🔴 Difícil (Hard)
- A IA usa algoritmo Minimax com profundidade 5
- Análise mais profunda e precisa
- Avalia 5 movimentos à frente
- Desafio para jogadores experientes

## 🎯 Características

✅ Suporte completo a regras de xadrez:
- Movimentos especiais (en passant, roque, promoção de peão)
- Detecção de xeque
- Detecção de xeque-mate
- Detecção de empate (afogamento)

✅ Cores clássicas de xadrez:
- Peças brancas (douradas) - #d4af37
- Peças pretas - #1a1a1a
- Casas claras - #f0d9b5
- Casas escuras - #8b4513

✅ Interface intuitiva:
- Mostra quando é a sua vez ou da IA
- Destaca movimentos válidos
- Mostra peças capturáveis com cores diferentes
- Sistema de som (se disponível)

## 📁 Arquivos

- `chess_new.py` - Motor principal do jogo e IA
- `play_chess.py` - Script para iniciar o jogo
- `test_ai.py` - Testes do sistema de IA

## 🛠️ Estrutura do Código

### Classe `ChessGame`
- Gerencia todo o jogo
- Valida movimentos
- Controla a IA

### Classe `ChessAI`
- Implementa algoritmo Minimax
- Avalia posições do tabuleiro
- Geração automática de movimentos

### Classe `Board`
- Representa o tabuleiro 8x8
- Armazena histórico de movimentos
- Gerencia estado do jogo

## 🎓 Conceitos Implementados

- **Minimax**: Algoritmo que explora todas as possibilidades de movimento
- **Avaliação de Posição**: Calcula valor estratégico da posição
- **Profundidade Limitada**: IA não analisa infinitamente, apenas N movimentos à frente
- **Poda Alpha-Beta**: Otimização para tornar IA mais rápida (pode ser adicionado)

## 📝 Exemplo de Uso via Python

```python
from chess_new import ChessGame, Color

# Criar jogo contra IA Médio, você com peças pretas
game = ChessGame(
    ai_enabled=True,
    ai_difficulty='medium',
    player_color=Color.BLACK
)

# Iniciar jogo
game.run()
```

## 🐛 Dicas para Melhorar o Desempenho

1. **Reduzir profundidade da IA**: Modifique `max_depth` em `ChessAI.__init__`
2. **Adicionar poda Alpha-Beta**: Otimizará a busca Minimax
3. **Cache de posições**: Armazene avaliações já calculadas
4. **Tabela de abertura**: Implemente sequências de abertura conhecidas

## 📜 Licença

Livre para uso pessoal e educacional.

---

**Divirta-se jogando xadrez!** ♔ vs 🤖 ♚
