import React, { useState,lazy, Suspense  } from 'react';
import api from '../services/api';

const ScanForm = () => {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      const response = await api.post('/scan', { url });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.msg || 'Scan failed');
    }
  };

  return (
    <div>
      <h2>URL Safety Scanner</h2>
      <form onSubmit={handleScan}>
        <input
          type="text"
          placeholder="Enter URL to scan"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          required
        />
        <button type="submit">Scan</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && (
        <div>
          <h3>Scan Results:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ScanForm;
