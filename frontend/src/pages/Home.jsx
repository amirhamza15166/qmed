import React, { useState } from 'react';
import Hero from '../components/hero/Hero';
import SymptomInput from '../components/analyzer/SymptomInput';
import AnalyzeButton from '../components/analyzer/AnalyzeButton';
import ResultCard from '../components/analyzer/ResultCard';
import { usePrediction } from '../hooks/usePrediction';
import { AlertCircle } from 'lucide-react';

const Home = () => {
  const [symptoms, setSymptoms] = useState('');
  const { analyze, loading, error, result, reset } = usePrediction();

  const handleAnalyze = () => {
    if (symptoms.trim().length < 10) return;
    analyze(symptoms);
  };

  const handleReset = () => {
    setSymptoms('');
    reset();
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Hero />
      
      <main id="analyzer" className="flex-1 w-full max-w-3xl mx-auto px-6 pb-24">
        {!result ? (
          <div className="bg-white rounded-2xl border border-gray-100 shadow-xl p-6 sm:p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-textPrimary">AI Symptom Assessment</h2>
              <p className="text-textSecondary mt-2">
                Our model is trained on a quantum pipeline to identify patterns in your symptoms.
              </p>
            </div>
            
            <SymptomInput 
              value={symptoms} 
              onChange={setSymptoms} 
              disabled={loading} 
            />
            
            {error && (
              <div className="mt-4 p-4 bg-error/10 text-error rounded-xl flex items-start gap-3">
                <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
            
            <div className="mt-8 flex justify-end">
              <AnalyzeButton 
                onClick={handleAnalyze} 
                loading={loading} 
                disabled={symptoms.trim().length < 10} 
              />
            </div>
          </div>
        ) : (
          <ResultCard result={result} onReset={handleReset} />
        )}
      </main>
    </div>
  );
};

export default Home;
