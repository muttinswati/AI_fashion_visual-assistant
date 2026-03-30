import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_BASE = "http://127.0.0.1:8000";

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const uploadImage = async () => {
    if (!file) return alert("Please select an image first!");
    
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API_BASE}/upload/`, formData);
      setResults(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Backend is not responding. Is Uvicorn running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>👗 AI Fashion Finder</h1>
      
      <div style={{ margin: '20px' }}>
        <input type="file" onChange={handleFileChange} />
        <button onClick={uploadImage} disabled={loading} style={{ padding: '10px 20px', cursor: 'pointer' }}>
          {loading ? "Processing..." : "Find Matches"}
        </button>
      </div>

      <hr />

      <div style={{ display: 'flex', justifyContent: 'space-around', marginTop: '20px' }}>
        {/* Left Side: Your Upload */}
        {preview && (
          <div style={{ width: '30%' }}>
            <h3>Your Image</h3>
            <img src={preview} alt="User" style={{ width: '100%', borderRadius: '10px' }} />
          </div>
        )}

        {/* Right Side: AI Results */}
        {results && (
          <div style={{ width: '60%' }}>
            <h3>Recommended Outfits</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
              {results.recommendations.map((imgName, index) => (
                <div key={index}>
                  <img 
                    src={`${API_BASE}/images/${imgName}`} 
                    alt="Match" 
                    style={{ width: '100%', borderRadius: '8px', border: '1px solid #ddd' }} 
                  />
                  <p>{imgName}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;