import React, { useState } from 'react';
import axios from 'axios';

const ScanForm = () => {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleScan = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    try {
      // Assume the backend is running on localhost:5000
      // and you have a valid JWT token stored in localStorage
      const token = localStorage.getItem("access_token");
      const response = await axios.post("http://localhost:5000/scan", { url }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.msg || "Scan failed");
    }
  };

  return (
    <div>
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
      { error && <div style={{color: 'red'}}>{error}</div> }
      { result && (
        <div>
          <h3>Scan Results:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      ) }
    </div>
  );
};

export default ScanForm;
