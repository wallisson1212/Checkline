import React, { useState, useEffect } from 'react';
import { Color, initializeBoard } from '../types';
import { ChessEngine } from '../engine/ChessEngine';
import { ChessAI } from '../engine/ChessAI';
import Square from './Square';
import './Board.css';

interface BoardProps {
  playerColor?: 'white' | 'black';
  difficulty?: 'très-fácil' | 'fácil' | 'médio' | 'difícil' | 'muito-difícil' | 'mestre';
  timeLimit?: number;
  onTimeUpdate?: (remainingSeconds: number) => void;
}

const Board: React.FC<BoardProps> = ({ playerColor = 'white', difficulty = 'médio', timeLimit = 10, onTimeUpdate }) => {
  const [engine] = useState(() => new ChessEngine(initializeBoard()));
  const [ai] = useState(() => new ChessAI(difficulty));
  const [board, setBoard] = useState(engine.getBoard());
  const [selectedSquare, setSelectedSquare] = useState<[number, number] | null>(null);
  const [validMoves, setValidMoves] = useState<Set<string>>(new Set());
  const [gameStatus, setGameStatus] = useState(engine.getGameStatus());
  const [currentPlayer, setCurrentPlayer] = useState(Color.WHITE);
  const [isAIThinking, setIsAIThinking] = useState(false);
  const [gameStarted, setGameStarted] = useState(false);
  const [timeExpired, setTimeExpired] = useState(false);

  const playerColorEnum = playerColor === 'white' ? Color.WHITE : Color.BLACK;
  const aiColor = playerColorEnum === Color.WHITE ? Color.BLACK : Color.WHITE;

  // Timer effect
  useEffect(() => {
    if (!gameStarted || gameStatus.gameOver || timeExpired) {
      return;
    }

    let remainingTime = timeLimit * 60;
    const timer = setInterval(() => {
      remainingTime -= 1;
      if (onTimeUpdate) {
        onTimeUpdate(remainingTime);
      }
      if (remainingTime <= 0) {
        setTimeExpired(true);
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [gameStarted, gameStatus.gameOver, timeExpired, onTimeUpdate]);

  // AI move effect
  useEffect(() => {
    if (gameStatus.gameOver || currentPlayer !== aiColor || isAIThinking || timeExpired) {
      return;
    }

    setIsAIThinking(true);

    const difficultyMap = {
      'très-fácil': 250,
      'fácil': 500,
      'médio': 750,
      'difícil': 1000,
      'muito-difícil': 1500,
      'mestre': 2000
    };

    const delay = difficultyMap[difficulty] || 750;

    const timer = setTimeout(() => {
      try {
        const aiMove = ai.getBestMove(engine, aiColor);
        
        if (aiMove) {
          const [fromX, fromY, toX, toY] = aiMove;
          const success = engine.makeMove(fromX, fromY, toX, toY);
          
          if (success) {
            setBoard(engine.getBoard());
            setSelectedSquare(null);
            setValidMoves(new Set());
            setCurrentPlayer(engine.getCurrentPlayer());
            setGameStatus(engine.getGameStatus());
          }
        }
      } finally {
        setIsAIThinking(false);
      }
    }, delay);

    return () => clearTimeout(timer);
  }, [currentPlayer, aiColor, gameStatus.gameOver, difficulty, timeExpired]);

  const handleSquareClick = (x: number, y: number) => {
    if (gameStatus.gameOver || currentPlayer !== playerColorEnum || isAIThinking || timeExpired) return;

    // Iniciar o jogo no primeiro movimento
    if (!gameStarted) {
      setGameStarted(true);
    }

    if (selectedSquare) {
      const [fromX, fromY] = selectedSquare;

      if (validMoves.has(`${x},${y}`)) {
        if (engine.makeMove(fromX, fromY, x, y)) {
          setBoard(engine.getBoard());
          setSelectedSquare(null);
          setValidMoves(new Set());
          setCurrentPlayer(engine.getCurrentPlayer());
          setGameStatus(engine.getGameStatus());
        }
      } else if (x === fromX && y === fromY) {
        setSelectedSquare(null);
        setValidMoves(new Set());
      } else {
        const piece = engine.getPiece(x, y);
        if (piece && piece.color === engine.getCurrentPlayer()) {
          setSelectedSquare([x, y]);
          const moves = engine.getValidMoves(x, y);
          setValidMoves(new Set(moves.map(([mx, my]) => `${mx},${my}`)));
        } else {
          setSelectedSquare(null);
          setValidMoves(new Set());
        }
      }
    } else {
      const piece = engine.getPiece(x, y);
      if (piece && piece.color === engine.getCurrentPlayer()) {
        setSelectedSquare([x, y]);
        const moves = engine.getValidMoves(x, y);
        setValidMoves(new Set(moves.map(([mx, my]) => `${mx},${my}`)));
      }
    }
  };

  return (
    <div className="board-container">
      <div className="board">
        {playerColor === 'black' 
          ? board.slice().reverse().map((row, y) =>
              row.slice().reverse().map((piece, x) => {
                const boardX = 7 - x;
                const boardY = 7 - y;
                const isLight = (boardX + boardY) % 2 === 0;
                const isSelected = selectedSquare ? selectedSquare[0] === boardX && selectedSquare[1] === boardY : false;
                const moveKey = `${boardX},${boardY}`;
                const isValidMove = validMoves.has(moveKey);
                const isCapture = isValidMove && piece !== null;

                return (
                  <Square
                    key={`${boardX}-${boardY}`}
                    piece={piece}
                    isLight={isLight}
                    x={boardX}
                    y={boardY}
                    isSelected={isSelected}
                    isValidMove={isValidMove}
                    isCapture={isCapture}
                    onClick={handleSquareClick}
                  />
                );
              })
            )
          : board.map((row, y) =>
              row.map((piece, x) => {
                const isLight = (x + y) % 2 === 0;
                const isSelected = selectedSquare ? selectedSquare[0] === x && selectedSquare[1] === y : false;
                const moveKey = `${x},${y}`;
                const isValidMove = validMoves.has(moveKey);
                const isCapture = isValidMove && piece !== null;

                return (
                  <Square
                    key={`${x}-${y}`}
                    piece={piece}
                    isLight={isLight}
                    x={x}
                    y={y}
                    isSelected={isSelected}
                    isValidMove={isValidMove}
                    isCapture={isCapture}
                    onClick={handleSquareClick}
                  />
                );
              })
            )
        }
      </div>
      
      {/* Checkmate Victory Modal */}
      {gameStatus.gameOver && gameStatus.winner && (
        <div className="checkmate-modal">
          <div className="checkmate-panel">
            <div className="checkmate-icon">
              {gameStatus.winner === Color.WHITE ? '♔' : '♚'}
            </div>
            <h2>{gameStatus.winner === Color.WHITE ? '♔ PEÇAS DOURADAS' : '♚ PEÇAS PRETAS'} VENCEM!</h2>
            <p className="checkmate-message">🎉 XEQUE-MATE! 🎉</p>
            <div className="checkmate-stats">
              <div className="stat">
                <span className="stat-label">Vencedor:</span>
                <span className="stat-value">{gameStatus.winner === Color.WHITE ? '♔ Brancas' : '♚ Pretas'}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Dificuldade:</span>
                <span className="stat-value">{difficulty}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Time Expired Modal */}
      {timeExpired && (
        <div className="time-expired-modal">
          <div className="time-expired-panel">
            <div className="time-expired-icon">⏱️</div>
            <h2>⏰ TEMPO EXPIRADO!</h2>
            <p className="time-message">Você não conseguiu terminar a partida a tempo.</p>
            <div className="time-stats">
              <div className="stat">
                <span className="stat-label">Dificuldade:</span>
                <span className="stat-value">{difficulty}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Limite de Tempo:</span>
                <span className="stat-value">{timeLimit} minuto{timeLimit !== 1 ? 's' : ''}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Board;
