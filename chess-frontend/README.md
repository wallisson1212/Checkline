# Xadrezzz - Chess Game Frontend

Um jogo de xadrez interativo desenvolvido em **React + TypeScript + Vite**.

## 🎮 Features

✅ **Jogo de Xadrez Completo**
- Movimentos válidos para todas as peças
- Sistema de xeque e xeque-mate
- Afogamento (stalemate)
- Roque (castling)
- Promoção de peão
- En passant

✅ **Interface Moderna**
- Design responsivo
- Tabuleiro 8x8 com cores alternadas
- Visualização clara de movimentos válidos
- Indicadores de xeque em tempo real

✅ **Funcionalidades**
- Novo jogo
- Desfazer movimentos
- Histórico de movimentos
- Detecção automática de fin de jogo

## 🚀 Instalação

```bash
cd chess-frontend
npm install
```

## 💻 Desenvolvimento

Para iniciar o servidor de desenvolvimento:

```bash
npm run dev
```

O jogo abrirá automaticamente em `http://localhost:3000`

## 🏗️ Build

Para criar a build de produção:

```bash
npm run build
```

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── Board.tsx       # Componente principal do tabuleiro
│   ├── Square.tsx      # Componente de cada casa
│   └── Square.css      # Estilos das casas
├── engine/
│   └── ChessEngine.ts  # Lógica do jogo de xadrez
├── types.ts            # Tipos TypeScript
├── App.tsx             # Componente raiz
├── App.css             # Estilos globais
├── index.css           # CSS base
└── main.tsx            # Entry point
```

## 🎯 Como Jogar

1. **Clique em uma peça** para selecioná-la (deve ser da cor do jogador atual)
2. **Clique em um quadrado destacado** para mover a peça
3. Os círculos mostram os movimentos legais
4. Clique em **Novo Jogo** para recomeçar
5. Pressione **ESC** para sair (em versões futuras)

## 🎨 Cores do Tabuleiro

- **Quadrados claros**: `#f0d9b5`
- **Quadrados escuros**: `#b58863`
- **Seleção**: `#baca44`
- **Movimento válido**: Destaque amarelo

## 🔧 Tecnologias

- **React 18** - Framework UI
- **TypeScript** - Type safety
- **Vite** - Build tool
- **CSS3** - Styling e animações

## 📝 Notas de Desenvolvimento

A lógica do jogo está completamente implementada em `ChessEngine.ts` com:
- Validação de movimentos legais
- Prevenção de deixar o rei em xeque
- Detecção de check/checkmate/stalemate
- Suporte a todas as regras especiais do xadrez

## 🐛 Debug

Para adicionar logs de debug, modifique o arquivo `ChessEngine.ts` conforme necessário.

## 📄 Licença

MIT

---

Desenvolvido com ❤️ em 2026
