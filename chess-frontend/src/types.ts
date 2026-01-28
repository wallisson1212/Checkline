export enum PieceType {
  PAWN = 'pw',
  KNIGHT = 'kn',
  BISHOP = 'bs',
  ROOK = 'rk',
  QUEEN = 'qn',
  KING = 'kg',
}

export enum Color {
  WHITE = 'w',
  BLACK = 'b',
}

export interface Piece {
  color: Color;
  type: PieceType;
  id: string;
}

export interface BoardSquare {
  piece: Piece | null;
  x: number;
  y: number;
}

export interface GameState {
  board: (Piece | null)[][];
  currentPlayer: Color;
  selectedSquare: [number, number] | null;
  validMoves: Set<string>;
  gameOver: boolean;
  winner: Color | null;
  isCheck: boolean;
  moveHistory: string[];
}

export const getPieceSymbol = (piece: Piece): string => {
  const symbols: Record<Color, Record<PieceType, string>> = {
    [Color.WHITE]: {
      [PieceType.PAWN]: '♙',
      [PieceType.KNIGHT]: '♘',
      [PieceType.BISHOP]: '♗',
      [PieceType.ROOK]: '♖',
      [PieceType.QUEEN]: '♕',
      [PieceType.KING]: '♔',
    },
    [Color.BLACK]: {
      [PieceType.PAWN]: '♟',
      [PieceType.KNIGHT]: '♞',
      [PieceType.BISHOP]: '♝',
      [PieceType.ROOK]: '♜',
      [PieceType.QUEEN]: '♛',
      [PieceType.KING]: '♚',
    },
  };
  return symbols[piece.color][piece.type];
};

export const createPiece = (color: Color, type: PieceType, id: string): Piece => ({
  color,
  type,
  id,
});

export const initializeBoard = (): (Piece | null)[][] => {
  const board: (Piece | null)[][] = Array(8).fill(null).map(() => Array(8).fill(null));

  // Peças pretas
  board[0][0] = createPiece(Color.BLACK, PieceType.ROOK, 'b-rook-0');
  board[0][1] = createPiece(Color.BLACK, PieceType.KNIGHT, 'b-knight-0');
  board[0][2] = createPiece(Color.BLACK, PieceType.BISHOP, 'b-bishop-0');
  board[0][3] = createPiece(Color.BLACK, PieceType.QUEEN, 'b-queen');
  board[0][4] = createPiece(Color.BLACK, PieceType.KING, 'b-king');
  board[0][5] = createPiece(Color.BLACK, PieceType.BISHOP, 'b-bishop-1');
  board[0][6] = createPiece(Color.BLACK, PieceType.KNIGHT, 'b-knight-1');
  board[0][7] = createPiece(Color.BLACK, PieceType.ROOK, 'b-rook-1');

  for (let x = 0; x < 8; x++) {
    board[1][x] = createPiece(Color.BLACK, PieceType.PAWN, `b-pawn-${x}`);
  }

  // Peças brancas
  for (let x = 0; x < 8; x++) {
    board[6][x] = createPiece(Color.WHITE, PieceType.PAWN, `w-pawn-${x}`);
  }

  board[7][0] = createPiece(Color.WHITE, PieceType.ROOK, 'w-rook-0');
  board[7][1] = createPiece(Color.WHITE, PieceType.KNIGHT, 'w-knight-0');
  board[7][2] = createPiece(Color.WHITE, PieceType.BISHOP, 'w-bishop-0');
  board[7][3] = createPiece(Color.WHITE, PieceType.QUEEN, 'w-queen');
  board[7][4] = createPiece(Color.WHITE, PieceType.KING, 'w-king');
  board[7][5] = createPiece(Color.WHITE, PieceType.BISHOP, 'w-bishop-1');
  board[7][6] = createPiece(Color.WHITE, PieceType.KNIGHT, 'w-knight-1');
  board[7][7] = createPiece(Color.WHITE, PieceType.ROOK, 'w-rook-1');

  return board;
};
