import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-white border-t border-gray-100 py-8 text-center text-sm text-textSecondary mt-auto">
      <p>© {new Date().getFullYear()} Q-MedAI. An AI-powered research and analysis system.</p>
      <p className="mt-2 max-w-2xl mx-auto px-6">
        Not for medical diagnosis or emergency treatment. Always consult a healthcare professional.
      </p>
    </footer>
  );
};

export default Footer;
