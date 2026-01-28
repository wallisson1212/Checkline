import React, { useState } from 'react';
import Board from './components/Board';
import Home from './components/Home';
import GameSetup from './components/GameSetup';
import type { GameSettings } from './components/GameSetup';
import './App.css';

type GameState = 'home' | 'setup' | 'playing';

const App: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>('home');
  const [gameSettings, setGameSettings] = useState<GameSettings | null>(null);
  const [remainingTime, setRemainingTime] = useState(0);

  const handleStartGame = () => {
    setGameState('setup');
  };

  const handleStartWithSettings = (settings: GameSettings) => {
    setGameSettings(settings);
    setRemainingTime(settings.timeLimit * 60);
    setGameState('playing');
  };

  const handleBackToHome = () => {
    setGameState('home');
    setGameSettings(null);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="app">
      {gameState === 'home' && (
        <Home onStartGame={handleStartGame} />
      )}
      {gameState === 'setup' && (
        <GameSetup 
          onStartWithSettings={handleStartWithSettings}
          onBack={handleBackToHome}
        />
      )}
      {gameState === 'playing' && gameSettings && (
        <div className="game-container">
          <main>
            <Board playerColor={gameSettings.playerColor} difficulty={gameSettings.difficulty} timeLimit={gameSettings.timeLimit} onTimeUpdate={setRemainingTime} />
          </main>
          <footer className="app-footer">
            <div className="footer-content">
              <h1>♔ Checkline ♚</h1>
              <div className="footer-controls">
                <div className="time-info">
                  ⏱️ {formatTime(remainingTime)}
                </div>
                <button className="back-btn" onClick={handleBackToHome}>
                  ← Voltar
                </button>
              </div>
            </div>
          </footer>
        </div>
      )}
    </div>
  );
};

export default App;
