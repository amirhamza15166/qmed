import React from 'react';

const SymptomInput = ({ value, onChange, disabled }) => {
  const maxLength = 5000;

  return (
    <div className="w-full">
      <label htmlFor="symptoms" className="block text-sm font-semibold text-textPrimary mb-2">
        Describe what you're experiencing in your own words.
      </label>
      <div className="relative">
        <textarea
          id="symptoms"
          className="w-full h-48 p-4 rounded-xl border border-gray-200 bg-white shadow-sm focus:border-primary focus:ring-4 focus:ring-primary/10 transition-all resize-none disabled:opacity-50 disabled:bg-gray-50"
          placeholder="I have had a severe headache for two days. I also feel nauseous and sensitive to bright light..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          maxLength={maxLength}
          disabled={disabled}
        />
        <div className="absolute bottom-4 right-4 text-xs font-medium text-textSecondary">
          {value.length} / {maxLength}
        </div>
      </div>
    </div>
  );
};

export default SymptomInput;
