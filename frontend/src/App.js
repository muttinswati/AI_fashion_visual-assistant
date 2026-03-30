import React, { useState } from "react";
import axios from "axios";

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
      setResults(null); // Reset results when new file is chosen
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
    <div
      style={{
        padding: "40px",
        textAlign: "center",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
        backgroundColor: "#000000",
        minHeight: "100vh",
      }}
    >
      <h1 style={{ color: "#e5e9ec", marginBottom: "30px" }}>
        👗 AI Fashion Recommender
      </h1>

      <div
        style={{
          backgroundColor: "#988585",
          padding: "20px",
          borderRadius: "15px",
          display: "inline-block",
          boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
        }}
      >
        <input
          type="file"
          onChange={handleFileChange}
          style={{ marginBottom: "10px" }}
        />
        <button
          onClick={uploadImage}
          disabled={loading}
          style={{
            padding: "12px 25px",
            cursor: "pointer",
            backgroundColor: "#308aa9",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontWeight: "bold",
            transition: "0.3s",
          }}
        >
          {loading ? "AI is Styling..." : "Complete My Outfit"}
        </button>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "50px",
          marginTop: "40px",
          flexWrap: "wrap",
        }}
      >
        {/* LEFT: YOUR UPLOAD */}
        {preview && (
          <div style={{ width: "300px", textAlign: "center" }}>
            <h3 style={{ color: "#7f8c8d" }}>Your Selection</h3>
            <div
              style={{
                backgroundColor: "#fff",
                padding: "10px",
                borderRadius: "15px",
                boxShadow: "0 10px 20px rgba(0,0,0,0.1)",
              }}
            >
              <img
                src={preview}
                alt="User"
                style={{
                  width: "100%",
                  borderRadius: "10px",
                  height: "350px",
                  objectFit: "cover",
                }}
              />
            </div>
          </div>
        )}

        {/* RIGHT: AI RECOMMENDATIONS */}
        {results && (
          <div style={{ flex: "1", maxWidth: "800px" }}>
            <h3 style={{ color: "#15b2be", textAlign: "left" }}>
              AI Styled Results
            </h3>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
                gap: "20px",
              }}
            >
              {results.recommendations.map((imgName, index) => (
                <div
                  key={index}
                  style={{
                    background: "#0e0101",
                    padding: "15px",
                    borderRadius: "12px",
                    boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
                    border: "4px solid #eee",
                  }}
                >
                  <div
                    style={{
                      backgroundColor: "#e9d7d7",
                      borderRadius: "8px",
                      overflow: "hidden",
                    }}
                  >
                    <img
                      src={`${API_BASE}/images/${imgName}`}
                      alt="Match"
                      style={{
                        width: "100%",
                        height: "200px",
                        objectFit: "contain", // FIX: Prevents stretching/blur
                        display: "block",
                      }}
                    />
                  </div>
                  <p
                    style={{
                      fontSize: "12px",
                      color: "#95a5a6",
                      marginTop: "10px",
                      fontWeight: "600",
                    }}
                  >
                    MATCHED ITEM
                  </p>
                  <p style={{ fontSize: "11px", color: "#bdc3c7" }}>
                    ID: {imgName}
                  </p>
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
