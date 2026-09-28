import React from 'react';
import { Activity, AlertTriangle, RefreshCcw } from 'lucide-react';

const ResultCard = ({ result, onReset }) => {
  if (!result) return null;

  const disease = typeof result === 'string' ? result : result.disease;

  return (
    <div className="w-full bg-white rounded-2xl border border-gray-100 shadow-xl p-8 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center gap-3 mb-6 pb-6 border-b border-gray-100">
        <div className="w-12 h-12 bg-success/10 rounded-full flex items-center justify-center text-success">
          <Activity className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-success uppercase tracking-wider">Analysis Complete</h3>
          <p className="text-textSecondary text-sm">Preliminary Prediction</p>
        </div>
      </div>
      
      <div className="text-center py-6">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-textPrimary">{disease}</h2>
      </div>

      <div className="mt-8 bg-warning/10 border border-warning/20 rounded-xl p-4 flex gap-4 text-warning">
        <AlertTriangle className="w-6 h-6 shrink-0 mt-0.5" />
        <p className="text-sm font-medium leading-relaxed">
          <strong>Medical Disclaimer:</strong> This result is an AI-generated preliminary prediction based on the symptoms provided. It is not a medical diagnosis and should not replace evaluation by a qualified healthcare professional.
        </p>
      </div>
      
      <div className="mt-8 flex justify-center">
        <button 
          onClick={onReset}
          className="flex items-center gap-2 px-6 py-3 text-sm font-semibold text-textSecondary hover:text-textPrimary bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <RefreshCcw className="w-4 h-4" />
          Start New Assessment
        </button>
      </div>
    </div>
  );
};

export default ResultCard;
