import React from 'react';
import { Piece, Color, getPieceSymbol } from '../types';
import './Square.css';

interface SquareProps {
  piece: Piece | null;
  isLight: boolean;
  x: number;
  y: number;
  isSelected: boolean;
  isValidMove: boolean;
  isCapture: boolean;
  onClick: (x: number, y: number) => void;
}

const Square: React.FC<SquareProps> = ({
  piece,
  isLight,
  x,
  y,
  isSelected,
  isValidMove,
  isCapture,
  onClick,
}) => {
  const handleClick = () => onClick(x, y);

  return (
    <div
      className={`square ${isLight ? 'light' : 'dark'} ${isSelected ? 'selected' : ''} ${
        isValidMove ? 'valid-move' : ''
      } ${isCapture ? 'capture' : ''}`}
      onClick={handleClick}
    >
      {piece && (
        <div className={`piece ${piece.color === Color.WHITE ? 'white' : 'black'}`}>
          {getPieceSymbol(piece)}
        </div>
      )}
    </div>
  );
};

export default Square;
