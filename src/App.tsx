import React from 'react';
import { MarketingDeck } from './components/MarketingDeck';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-[var(--color-bg)] text-[var(--color-ivory)]">
      <MarketingDeck />
    </div>
  );
};

export default App;
