import { useState } from 'react';
import { predictSymptoms } from '../services/api';

export const usePrediction = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const analyze = async (symptoms) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await predictSymptoms(symptoms);
      setResult(data.prediction);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setResult(null);
    setError(null);
  };

  return { analyze, loading, error, result, reset };
};
