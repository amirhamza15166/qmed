import React from 'react';
import { Activity } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-white border-b border-gray-100 py-4 px-6 sm:px-10 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center gap-2 text-primary font-bold text-xl">
        <Activity className="w-6 h-6 text-primary" />
        <span>Q-MedAI</span>
      </div>
      <div className="hidden sm:flex items-center gap-6 text-sm font-medium text-textSecondary">
        <a href="#how-it-works" className="hover:text-primary transition-colors">How it works</a>
        <a href="#analyzer" className="hover:text-primary transition-colors">Analyzer</a>
      </div>
    </nav>
  );
};

export default Navbar;
