import React from 'react';
import { Shield, Zap, Lock } from 'lucide-react';

const Hero = () => {
  return (
    <section className="py-20 px-6 max-w-4xl mx-auto text-center">
      <p className="text-accent font-semibold tracking-wide uppercase text-sm mb-4">
        Quantum-enhanced healthcare intelligence
      </p>
      <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-textPrimary tracking-tight mb-6">
        Understand your symptoms.<br/>Explore what they may indicate.
      </h1>
      <p className="text-lg sm:text-xl text-textSecondary mb-10 max-w-2xl mx-auto">
        Describe how you feel in your own words. Our AI, powered by Quantum Machine Learning, analyzes your text to provide preliminary insights.
      </p>
      
      <div className="flex flex-wrap justify-center gap-6 sm:gap-10 text-sm font-medium text-textSecondary">
        <div className="flex items-center gap-2">
          <Zap className="w-5 h-5 text-secondary" />
          Quantum ML
        </div>
        <div className="flex items-center gap-2">
          <Lock className="w-5 h-5 text-secondary" />
          Privacy Focused
        </div>
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5 text-secondary" />
          Research Driven
        </div>
      </div>
    </section>
  );
};

export default Hero;
