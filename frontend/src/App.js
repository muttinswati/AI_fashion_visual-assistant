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
      setResults(null); // Reset results when a new file is chosen
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
          style={{ marginBottom: "10px", color: "white" }}
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
            opacity: loading ? 0.7 : 1,
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

        {/* RIGHT: AI RECOMMENDATIONS (Category-Based) */}
        {results && results.recommendations && (
          <div style={{ flex: "1", maxWidth: "900px" }}>
            <h3
              style={{
                color: "#15b2be",
                textAlign: "left",
                marginBottom: "25px",
              }}
            >
              AI Styled Results
            </h3>

            {Object.keys(results.recommendations).map((category) => (
              <div
                key={category}
                style={{ marginBottom: "40px", textAlign: "left" }}
              >
                <h4
                  style={{
                    color: "#e5e9ec",
                    borderBottom: "1px solid #333",
                    paddingBottom: "8px",
                    textTransform: "uppercase",
                    letterSpacing: "1px",
                    fontSize: "14px",
                  }}
                >
                  {category} Suggestions
                </h4>
                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "repeat(auto-fill, minmax(180px, 1fr))",
                    gap: "20px",
                    marginTop: "15px",
                  }}
                >
                  {results.recommendations[category].map((imgName, index) => (
                    <div
                      key={`${category}-${index}`}
                      style={{
                        background: "#0e0101",
                        padding: "15px",
                        borderRadius: "12px",
                        boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
                        border: "2px solid #222",
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
                            objectFit: "contain",
                            display: "block",
                          }}
                        />
                      </div>
                      <p
                        style={{
                          fontSize: "12px",
                          color: "#308aa9",
                          marginTop: "10px",
                          fontWeight: "600",
                        }}
                      >
                        {category.toUpperCase()} MATCH
                      </p>
                      <p style={{ fontSize: "11px", color: "#bdc3c7" }}>
                        ID: {imgName}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
