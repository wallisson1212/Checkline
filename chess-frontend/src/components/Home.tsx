import React, { useEffect, useRef } from 'react';
import './Home.css';

interface HomeProps {
  onStartGame: () => void;
}

const Home: React.FC<HomeProps> = ({ onStartGame }) => {
  const instructionBlocksRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Criar observer para animar elementos quando ficam visíveis
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        } else {
          entry.target.classList.remove('visible');
        }
      });
    }, observerOptions);

    // Observar todos os blocos de instrução
    const blocks = document.querySelectorAll('.instruction-block, .ready-to-play');
    blocks.forEach((block) => {
      observer.observe(block);
    });

    return () => {
      blocks.forEach((block) => {
        observer.unobserve(block);
      });
    };
  }, []);

  return (
    <div className="home-page">
      <div className="home-container">
        <div className="home-content">
          <div className="logo">♔ Checkline ♚</div>
          <h1>Seja bem-vindo ao Checkline - Divirta-se</h1>
          <button className="start-button" onClick={onStartGame}>
            🎮 Começar Novo Jogo
          </button>
          <div className="scroll-hint">⬇️ Role para aprender</div>
        </div>
      </div>

      <div className="learn-more-section">
        <div className="learn-content" ref={instructionBlocksRef}>
          <h2>Como Jogar</h2>
          
          <div className="instruction-block">
            <h3>📋 O Básico</h3>
            <p>Xadrez é um jogo de estratégia entre dois jogadores. Cada um controla 16 peças com o objetivo de derrotar o rei adversário.</p>
          </div>

          <div className="instruction-block">
            <h3>🎯 Como Mover</h3>
            <ul>
              <li><strong>Clique em uma peça</strong> para selecioná-la (deve ser sua cor)</li>
              <li><strong>Círculos claros</strong> mostram onde você pode mover</li>
              <li><strong>Clique em um local destacado</strong> para completar o movimento</li>
              <li><strong>Círculos vermelhos</strong> indicam capturas disponíveis</li>
            </ul>
          </div>

          <div className="instruction-block">
            <h3>♟️ As Peças</h3>
            <div className="pieces-list">
              <div className="piece-desc">
                <span className="piece-emoji">♙</span>
                <div>
                  <strong>Peão</strong>
                  <p>Move 1 casa à frente (2 no primeiro movimento). Captura na diagonal.</p>
                </div>
              </div>
              <div className="piece-desc">
                <span className="piece-emoji">♘</span>
                <div>
                  <strong>Cavalo</strong>
                  <p>Move em L (2 casas em uma direção, 1 perpendicular). Pode pular peças.</p>
                </div>
              </div>
              <div className="piece-desc">
                <span className="piece-emoji">♗</span>
                <div>
                  <strong>Bispo</strong>
                  <p>Move na diagonal quantas casas quiser.</p>
                </div>
              </div>
              <div className="piece-desc">
                <span className="piece-emoji">♖</span>
                <div>
                  <strong>Torre</strong>
                  <p>Move horizontal ou verticalmente quantas casas quiser.</p>
                </div>
              </div>
              <div className="piece-desc">
                <span className="piece-emoji">♕</span>
                <div>
                  <strong>Rainha</strong>
                  <p>Move em qualquer direção quantas casas quiser. É a peça mais poderosa!</p>
                </div>
              </div>
              <div className="piece-desc">
                <span className="piece-emoji">♔</span>
                <div>
                  <strong>Rei</strong>
                  <p>Move 1 casa em qualquer direção. É o objetivo do jogo protegê-lo!</p>
                </div>
              </div>
            </div>
          </div>

          <div className="instruction-block">
            <h3>⚔️ Condições do Jogo</h3>
            <ul>
              <li><strong>Xeque:</strong> Seu rei está sendo ameaçado. Você deve se defender!</li>
              <li><strong>Xeque-mate:</strong> Seu rei está em xeque e não há como escapar. Fim do jogo!</li>
              <li><strong>Afogamento:</strong> Nenhum movimento legal disponível, mas o rei não está em xeque. Resultado em empate!</li>
            </ul>
          </div>

          <div className="instruction-block">
            <h3>💡 Dicas Para Iniciantes</h3>
            <ul>
              <li>Sempre proteja o seu rei - ele é o mais importante!</li>
              <li>Desenvolva suas peças menores no início do jogo</li>
              <li>Controle o centro do tabuleiro (as 4 casas do meio)</li>
              <li>Não coloque peças valiosas onde podem ser capturadas facilmente</li>
              <li>Procure por oportunidades de xeque-mate</li>
              <li>Domine os movimentos especiais: castelo, en passant e promoção</li>
            </ul>
          </div>

          <div className="ready-to-play">
            <p>Pronto para começar a jogar?</p>
            <button className="start-button large" onClick={onStartGame}>
              🎮 Começar Novo Jogo
            </button>
          </div>

          <footer className="copyright-footer">
            <p>© 2026 Checkline - Desenvolvido por Wallisson Elizeu</p>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default Home;
