import React from 'react';

interface HeaderProps {
  onNavClick: (targetId: string) => void;
}

export const Header = ({ onNavClick }: HeaderProps) => {
  const handleClick = (e: React.MouseEvent<HTMLElement>, id: string) => {
    e.preventDefault();
    onNavClick(id);
  };
  
  return (
    <header className="header">
      <div className="header-container">
        <div 
          className="brand-area" 
          style={{ cursor: 'pointer' }} 
          onClick={(e) => handleClick(e, 'top')}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => e.key === 'Enter' && handleClick(e as unknown as React.MouseEvent<HTMLElement>, 'top')}
        >
          <span className="brand-name">MedGuide</span>
          <span className="brand-desc">Medical Evidence Assistant</span>
        </div>
        <div className="nav-area">
          <nav className="nav-links">
            <a href="#guidelines" onClick={(e) => handleClick(e, 'guidelines')}>Guidelines</a>
            <a href="#how-it-works" onClick={(e) => handleClick(e, 'how-it-works')}>How it works</a>
            <a href="#about" onClick={(e) => handleClick(e, 'about')}>About</a>
          </nav>
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span>System ready</span>
          </div>
        </div>
      </div>
    </header>
  );
};
