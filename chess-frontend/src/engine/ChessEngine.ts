import { Color, PieceType, Piece } from '../types';

export class ChessEngine {
  private board: (Piece | null)[][];
  private currentPlayer: Color = Color.WHITE;
  private whiteKingMoved: boolean = false;
  private blackKingMoved: boolean = false;
  private whiteRookAMoved: boolean = false;
  private whiteRookHMoved: boolean = false;
  private blackRookAMoved: boolean = false;
  private blackRookHMoved: boolean = false;
  private moveHistory: string[] = [];

  constructor(board: (Piece | null)[][]) {
    this.board = board.map(row => [...row]);
  }

  getBoard(): (Piece | null)[][] {
    return this.board.map(row => [...row]);
  }

  getCurrentPlayer(): Color {
    return this.currentPlayer;
  }

  getPiece(x: number, y: number): Piece | null {
    if (x >= 0 && x < 8 && y >= 0 && y < 8) {
      return this.board[y][x];
    }
    return null;
  }

  isSquareEmpty(x: number, y: number): boolean {
    return this.getPiece(x, y) === null;
  }

  findKing(color: Color): [number, number] | null {
    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        const piece = this.getPiece(x, y);
        if (piece && piece.color === color && piece.type === PieceType.KING) {
          return [x, y];
        }
      }
    }
    return null;
  }

  private getPawnMoves(x: number, y: number, piece: Piece): [number, number][] {
    const moves: [number, number][] = [];
    const direction = piece.color === Color.WHITE ? -1 : 1;
    const startRow = piece.color === Color.WHITE ? 6 : 1;

    const nextY = y + direction;
    if (nextY >= 0 && nextY < 8 && this.isSquareEmpty(x, nextY)) {
      moves.push([x, nextY]);

      if (y === startRow) {
        const nextNextY = y + 2 * direction;
        if (this.isSquareEmpty(x, nextNextY)) {
          moves.push([x, nextNextY]);
        }
      }
    }

    for (const dx of [-1, 1]) {
      const captureX = x + dx;
      const captureY = y + direction;
      if (captureX >= 0 && captureX < 8 && captureY >= 0 && captureY < 8) {
        const target = this.getPiece(captureX, captureY);
        if (target && target.color !== piece.color) {
          moves.push([captureX, captureY]);
        }
      }
    }

    return moves;
  }

  private getKnightMoves(x: number, y: number, piece: Piece): [number, number][] {
    const moves: [number, number][] = [];
    const knightMoves = [
      [-2, -1], [-2, 1], [-1, -2], [-1, 2],
      [1, -2], [1, 2], [2, -1], [2, 1],
    ];

    for (const [dx, dy] of knightMoves) {
      const nx = x + dx;
      const ny = y + dy;
      if (nx >= 0 && nx < 8 && ny >= 0 && ny < 8) {
        const target = this.getPiece(nx, ny);
        if (!target || target.color !== piece.color) {
          moves.push([nx, ny]);
        }
      }
    }

    return moves;
  }

  private getBishopMoves(x: number, y: number, piece: Piece): [number, number][] {
    const moves: [number, number][] = [];
    const directions = [[-1, -1], [-1, 1], [1, -1], [1, 1]];

    for (const [dx, dy] of directions) {
      let nx = x + dx;
      let ny = y + dy;
      while (nx >= 0 && nx < 8 && ny >= 0 && ny < 8) {
        const target = this.getPiece(nx, ny);
        if (!target) {
          moves.push([nx, ny]);
        } else if (target.color !== piece.color) {
          moves.push([nx, ny]);
          break;
        } else {
          break;
        }
        nx += dx;
        ny += dy;
      }
    }

    return moves;
  }

  private getRookMoves(x: number, y: number, piece: Piece): [number, number][] {
    const moves: [number, number][] = [];
    const directions = [[-1, 0], [1, 0], [0, -1], [0, 1]];

    for (const [dx, dy] of directions) {
      let nx = x + dx;
      let ny = y + dy;
      while (nx >= 0 && nx < 8 && ny >= 0 && ny < 8) {
        const target = this.getPiece(nx, ny);
        if (!target) {
          moves.push([nx, ny]);
        } else if (target.color !== piece.color) {
          moves.push([nx, ny]);
          break;
        } else {
          break;
        }
        nx += dx;
        ny += dy;
      }
    }

    return moves;
  }

  private getQueenMoves(x: number, y: number, piece: Piece): [number, number][] {
    return [...this.getRookMoves(x, y, piece), ...this.getBishopMoves(x, y, piece)];
  }

  private getKingMoves(x: number, y: number, piece: Piece): [number, number][] {
    const moves: [number, number][] = [];

    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        if (dx === 0 && dy === 0) continue;
        const nx = x + dx;
        const ny = y + dy;
        if (nx >= 0 && nx < 8 && ny >= 0 && ny < 8) {
          const target = this.getPiece(nx, ny);
          if (!target || target.color !== piece.color) {
            moves.push([nx, ny]);
          }
        }
      }
    }

    // Castling
    if (piece.color === Color.WHITE && !this.whiteKingMoved && y === 7 && x === 4) {
      if (!this.whiteRookHMoved && this.isSquareEmpty(5, 7) && this.isSquareEmpty(6, 7)) {
        const rook = this.getPiece(7, 7);
        if (rook && rook.type === PieceType.ROOK) {
          moves.push([6, 7]);
        }
      }
      if (!this.whiteRookAMoved && this.isSquareEmpty(1, 7) && this.isSquareEmpty(2, 7) && this.isSquareEmpty(3, 7)) {
        const rook = this.getPiece(0, 7);
        if (rook && rook.type === PieceType.ROOK) {
          moves.push([2, 7]);
        }
      }
    } else if (piece.color === Color.BLACK && !this.blackKingMoved && y === 0 && x === 4) {
      if (!this.blackRookHMoved && this.isSquareEmpty(5, 0) && this.isSquareEmpty(6, 0)) {
        const rook = this.getPiece(7, 0);
        if (rook && rook.type === PieceType.ROOK) {
          moves.push([6, 0]);
        }
      }
      if (!this.blackRookAMoved && this.isSquareEmpty(1, 0) && this.isSquareEmpty(2, 0) && this.isSquareEmpty(3, 0)) {
        const rook = this.getPiece(0, 0);
        if (rook && rook.type === PieceType.ROOK) {
          moves.push([2, 0]);
        }
      }
    }

    return moves;
  }

  getValidMoves(x: number, y: number): [number, number][] {
    const piece = this.getPiece(x, y);
    if (!piece || piece.color !== this.currentPlayer) {
      return [];
    }

    let moves: [number, number][] = [];

    switch (piece.type) {
      case PieceType.PAWN:
        moves = this.getPawnMoves(x, y, piece);
        break;
      case PieceType.KNIGHT:
        moves = this.getKnightMoves(x, y, piece);
        break;
      case PieceType.BISHOP:
        moves = this.getBishopMoves(x, y, piece);
        break;
      case PieceType.ROOK:
        moves = this.getRookMoves(x, y, piece);
        break;
      case PieceType.QUEEN:
        moves = this.getQueenMoves(x, y, piece);
        break;
      case PieceType.KING:
        moves = this.getKingMoves(x, y, piece);
        break;
    }

    return moves.filter(([toX, toY]) => !this.moveLeaveKingInCheck(x, y, toX, toY));
  }

  private isUnderAttack(x: number, y: number, byColor: Color): boolean {
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const piece = this.getPiece(col, row);
        if (piece && piece.color === byColor) {
          const moves = this.getPseudoLegalMoves(col, row, piece);
          if (moves.some(([mx, my]) => mx === x && my === y)) {
            return true;
          }
        }
      }
    }
    return false;
  }

  private getPseudoLegalMoves(x: number, y: number, piece: Piece): [number, number][] {
    switch (piece.type) {
      case PieceType.PAWN:
        return this.getPawnMoves(x, y, piece);
      case PieceType.KNIGHT:
        return this.getKnightMoves(x, y, piece);
      case PieceType.BISHOP:
        return this.getBishopMoves(x, y, piece);
      case PieceType.ROOK:
        return this.getRookMoves(x, y, piece);
      case PieceType.QUEEN:
        return this.getQueenMoves(x, y, piece);
      case PieceType.KING: {
        const moves: [number, number][] = [];
        for (let dx = -1; dx <= 1; dx++) {
          for (let dy = -1; dy <= 1; dy++) {
            if (dx === 0 && dy === 0) continue;
            const nx = x + dx;
            const ny = y + dy;
            if (nx >= 0 && nx < 8 && ny >= 0 && ny < 8) {
              const target = this.getPiece(nx, ny);
              if (!target || target.color !== piece.color) {
                moves.push([nx, ny]);
              }
            }
          }
        }
        return moves;
      }
      default:
        return [];
    }
  }

  moveLeaveKingInCheck(fromX: number, fromY: number, toX: number, toY: number): boolean {
    const piece = this.getPiece(fromX, fromY);
    if (!piece) return true;

    const captured = this.getPiece(toX, toY);

    this.board[toY][toX] = piece;
    this.board[fromY][fromX] = null;

    const kingPos = this.findKing(piece.color);
    const opponent = piece.color === Color.WHITE ? Color.BLACK : Color.WHITE;
    const inCheck = kingPos ? this.isUnderAttack(kingPos[0], kingPos[1], opponent) : true;

    this.board[fromY][fromX] = piece;
    this.board[toY][toX] = captured;

    return inCheck;
  }

  makeMove(fromX: number, fromY: number, toX: number, toY: number): boolean {
    const piece = this.getPiece(fromX, fromY);
    if (!piece || piece.color !== this.currentPlayer) {
      return false;
    }

    const validMoves = this.getValidMoves(fromX, fromY);
    if (!validMoves.some(([x, y]) => x === toX && y === toY)) {
      return false;
    }

    this.board[toY][toX] = piece;
    this.board[fromY][fromX] = null;

    // Handle special moves
    if (piece.type === PieceType.PAWN) {
      if ((piece.color === Color.WHITE && toY === 0) || (piece.color === Color.BLACK && toY === 7)) {
        piece.type = PieceType.QUEEN;
      }
    }

    if (piece.type === PieceType.KING) {
      if (piece.color === Color.WHITE) {
        this.whiteKingMoved = true;
      } else {
        this.blackKingMoved = true;
      }

      if (fromX === 4 && toX === 6) {
        const rook = this.getPiece(7, toY);
        if (rook) {
          this.board[toY][5] = rook;
          this.board[toY][7] = null;
        }
      } else if (fromX === 4 && toX === 2) {
        const rook = this.getPiece(0, toY);
        if (rook) {
          this.board[toY][3] = rook;
          this.board[toY][0] = null;
        }
      }
    } else if (piece.type === PieceType.ROOK) {
      if (piece.color === Color.WHITE) {
        if (fromX === 0) this.whiteRookAMoved = true;
        else if (fromX === 7) this.whiteRookHMoved = true;
      } else {
        if (fromX === 0) this.blackRookAMoved = true;
        else if (fromX === 7) this.blackRookHMoved = true;
      }
    }

    this.moveHistory.push(`${String.fromCharCode(97 + fromX)}${8 - fromY}-${String.fromCharCode(97 + toX)}${8 - toY}`);
    this.currentPlayer = this.currentPlayer === Color.WHITE ? Color.BLACK : Color.WHITE;

    return true;
  }

  isInCheck(color: Color): boolean {
    const kingPos = this.findKing(color);
    if (!kingPos) return false;
    const opponent = color === Color.WHITE ? Color.BLACK : Color.WHITE;
    return this.isUnderAttack(kingPos[0], kingPos[1], opponent);
  }

  hasLegalMoves(color: Color): boolean {
    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        const piece = this.getPiece(x, y);
        if (piece && piece.color === color) {
          if (this.getValidMoves(x, y).length > 0) {
            return true;
          }
        }
      }
    }
    return false;
  }

  getGameStatus(): { gameOver: boolean; winner: Color | null; isCheck: boolean } {
    const currentInCheck = this.isInCheck(this.currentPlayer);
    const hasLegalMoves = this.hasLegalMoves(this.currentPlayer);

    if (!hasLegalMoves) {
      if (currentInCheck) {
        const opponent = this.currentPlayer === Color.WHITE ? Color.BLACK : Color.WHITE;
        return { gameOver: true, winner: opponent, isCheck: true };
      } else {
        return { gameOver: true, winner: null, isCheck: false };
      }
    }

    return { gameOver: false, winner: null, isCheck: currentInCheck };
  }
}
