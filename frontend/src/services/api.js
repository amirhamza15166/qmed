import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || (import.meta.env.PROD ? '' : 'http://127.0.0.1:8000');

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 15000, // 15 second timeout to prevent infinite loading
  headers: {
    'Content-Type': 'application/json',
  },
});

export const predictSymptoms = async (symptoms) => {
  try {
    const response = await apiClient.post('/predict', { symptoms });
    return response.data;
  } catch (error) {
    if (error.code === 'ECONNABORTED') {
      throw new Error('The prediction is taking longer than expected. Please try again.');
    }
    if (error.response) {
      throw new Error(error.response.data.error || error.response.data.detail || 'Failed to analyze symptoms.');
    } else if (error.request) {
      throw new Error('Prediction service is currently unavailable. Please make sure the backend server is running and try again.');
    } else {
      throw new Error('An unexpected error occurred.');
    }
  }
};
