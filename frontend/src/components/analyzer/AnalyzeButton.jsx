import React from 'react';
import { Loader2 } from 'lucide-react';

const AnalyzeButton = ({ onClick, disabled, loading }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className="w-full sm:w-auto px-8 py-4 bg-primary hover:bg-blue-700 text-white font-semibold rounded-xl shadow-lg shadow-primary/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
    >
      {loading ? (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Analyzing your symptoms...
        </>
      ) : (
        'Analyze Symptoms'
      )}
    </button>
  );
};

export default AnalyzeButton;
