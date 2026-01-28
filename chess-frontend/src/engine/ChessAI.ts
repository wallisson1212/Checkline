import { ChessEngine } from './ChessEngine';
import { Color, PieceType } from '../types';

export class ChessAI {
  private difficulty: 'très-fácil' | 'fácil' | 'médio' | 'difícil' | 'muito-difícil' | 'mestre';

  // Valores das peças para avaliação
  private PIECE_VALUES: Record<PieceType, number> = {
    [PieceType.PAWN]: 1,
    [PieceType.KNIGHT]: 3,
    [PieceType.BISHOP]: 3,
    [PieceType.ROOK]: 5,
    [PieceType.QUEEN]: 9,
    [PieceType.KING]: 1000,
  };

  constructor(difficulty: 'très-fácil' | 'fácil' | 'médio' | 'difícil' | 'muito-difícil' | 'mestre' = 'médio') {
    this.difficulty = difficulty;
  }

  /**
   * Retorna o melhor movimento para a cor dada
   */
  getBestMove(engine: ChessEngine, color: Color): [number, number, number, number] | null {
    // Coletar todos os movimentos possíveis
    const allMoves = this.getAllValidMoves(engine, color);

    if (allMoves.length === 0) {
      return null;
    }

    // Très-fácil: retorna um movimento aleatório
    if (this.difficulty === 'très-fácil') {
      const randomIndex = Math.floor(Math.random() * allMoves.length);
      return allMoves[randomIndex];
    }

    // Médio e Difícil: avaliar cada movimento
    let bestMove = allMoves[0];
    let bestScore = -Infinity;

    for (const move of allMoves) {
      const score = this.evaluateMove(engine, move, color);
      if (score > bestScore) {
        bestScore = score;
        bestMove = move;
      }
    }

    return bestMove;
  }

  /**
   * Avalia um movimento específico
   */
  private evaluateMove(
    engine: ChessEngine,
    [fromX, fromY, toX, toY]: [number, number, number, number],
    color: Color
  ): number {
    let score = 0;

    // 1. Capturar peças é muito bom
    const targetPiece = engine.getPiece(toX, toY);
    if (targetPiece) {
      score += this.PIECE_VALUES[targetPiece.type] * 10;
    }

    // 2. Proteger peças amigas
    const piece = engine.getPiece(fromX, fromY);
    if (piece) {
      score += this.PIECE_VALUES[piece.type] * 0.5;
    }

    // 3. Bônus por controlar o centro
    const centerSquares = [[3, 3], [3, 4], [4, 3], [4, 4]];
    for (const [cx, cy] of centerSquares) {
      if (toX === cx && toY === cy && !targetPiece) {
        score += 5;
      }
    }

    // 4. Bonus por avançar peões
    if (piece && piece.type === PieceType.PAWN) {
      if (color === Color.WHITE && toY < fromY) {
        score += (fromY - toY) * 2;
      } else if (color === Color.BLACK && toY > fromY) {
        score += (toY - fromY) * 2;
      }
    }

    return score;
  }

  /**
   * Coletar todos os movimentos válidos para uma cor
   */
  private getAllValidMoves(engine: ChessEngine, color: Color): [number, number, number, number][] {
    const moves: [number, number, number, number][] = [];
    const board = engine.getBoard();

    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        const piece = board[y][x];
        if (piece && piece.color === color) {
          const validMoves = engine.getValidMoves(x, y);
          for (const [toX, toY] of validMoves) {
            moves.push([x, y, toX, toY]);
          }
        }
      }
    }

    return moves;
  }
}
