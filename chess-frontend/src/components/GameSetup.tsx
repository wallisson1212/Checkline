import React, { useState } from 'react';
import './GameSetup.css';

interface GameSetupProps {
  onStartWithSettings: (settings: GameSettings) => void;
  onBack: () => void;
}

export interface GameSettings {
  difficulty: 'très-fácil' | 'fácil' | 'médio' | 'difícil' | 'muito-difícil' | 'mestre';
  playerColor: 'white' | 'black';
  timeLimit: number; // em minutos
}

const GameSetup: React.FC<GameSetupProps> = ({ onStartWithSettings, onBack }) => {
  const [difficulty, setDifficulty] = useState<'très-fácil' | 'fácil' | 'médio' | 'difícil' | 'muito-difícil' | 'mestre'>('médio');
  const [playerColor, setPlayerColor] = useState<'white' | 'black'>('white');
  const [timeLimit, setTimeLimit] = useState(10);

  const handleStart = () => {
    onStartWithSettings({
      difficulty,
      playerColor,
      timeLimit
    });
  };

  return (
    <div className="game-setup-overlay">
      <div className="game-setup-panel">
        <h2>⚙️ Configurar Partida</h2>
        
        {/* Dificuldade */}
        <div className="setup-section">
          <h3>Nível de Dificuldade</h3>
          <div className="difficulty-display-label">
            <span className="difficulty-value">
              {difficulty === 'très-fácil' ? '🟢🟢 Muito Fácil' : 
               difficulty === 'fácil' ? '🟢 Fácil' : 
               difficulty === 'médio' ? '🟡 Médio' : 
               difficulty === 'difícil' ? '🔴 Difícil' :
               difficulty === 'muito-difícil' ? '🔴🔴 Muito Difícil' : '🔴🔴🔴 Mestre'}
            </span>
          </div>
          <div className="difficulty-control">
            <input
              type="range"
              min="1"
              max="6"
              value={
                difficulty === 'très-fácil' ? 1 :
                difficulty === 'fácil' ? 2 :
                difficulty === 'médio' ? 3 :
                difficulty === 'difícil' ? 4 :
                difficulty === 'muito-difícil' ? 5 : 6
              }
              onChange={(e) => {
                const val = parseInt(e.target.value);
                const diffMap = {
                  1: 'très-fácil',
                  2: 'fácil',
                  3: 'médio',
                  4: 'difícil',
                  5: 'muito-difícil',
                  6: 'mestre'
                } as const;
                setDifficulty(diffMap[val as keyof typeof diffMap]);
              }}
              className="difficulty-slider"
            />
          </div>
        </div>

        {/* Cor das Peças */}
        <div className="setup-section">
          <h3>Sua Cor</h3>
          <div className="color-options">
            <label className={`option ${playerColor === 'white' ? 'selected' : ''}`}>
              <input
                type="radio"
                name="color"
                value="white"
                checked={playerColor === 'white'}
                onChange={(e) => setPlayerColor(e.target.value as 'white' | 'black')}
              />
              <span>♔ Dourada</span>
            </label>
            <label className={`option ${playerColor === 'black' ? 'selected' : ''}`}>
              <input
                type="radio"
                name="color"
                value="black"
                checked={playerColor === 'black'}
                onChange={(e) => setPlayerColor(e.target.value as 'white' | 'black')}
              />
              <span>♚ Preta</span>
            </label>
          </div>
        </div>

        {/* Tempo da Partida */}
        <div className="setup-section">
          <h3>Tempo da Partida</h3>
          <div className="time-control">
            <input
              type="range"
              min="1"
              max="60"
              value={timeLimit}
              onChange={(e) => setTimeLimit(parseInt(e.target.value))}
              className="time-slider"
            />
            <div className="time-display">
              <span className="time-value">{timeLimit}</span>
              <span className="time-unit">minuto{timeLimit !== 1 ? 's' : ''}</span>
            </div>
          </div>
        </div>

        {/* Botões */}
        <div className="setup-buttons">
          <button className="btn-back" onClick={onBack}>
            ← Voltar
          </button>
          <button className="btn-start" onClick={handleStart}>
            🎮 Começar Partida
          </button>
        </div>
      </div>
    </div>
  );
};

export default GameSetup;
