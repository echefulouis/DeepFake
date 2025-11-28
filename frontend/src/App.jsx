import { useState } from 'react'
import axios from 'axios'
import { FiShield, FiCheck, FiX, FiLoader, FiFolder, FiEye } from 'react-icons/fi'
import './App.css'

function App() {
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => setImage(e.target.result)
      reader.readAsDataURL(file)
      setResult(null)
      setError(null)
    }
  }

  const uploadImage = async () => {
    if (!image) return
    
    setLoading(true)
    setError(null)
    
    try {
      const base64 = image.split(',')[1]
      const response = await axios.post(`${import.meta.env.VITE_API_ENDPOINT}upload`, {
        image: base64
      })
      

      setResult(response.data)
    } catch (error) {
      console.error('Upload failed:', error)
      setError(error.response?.data?.error || 'Upload failed')
    }
    setLoading(false)
  }

  return (
    <div className="app">
      <div className="header">
        <FiShield className="header-icon" />
        <h1>Deepfake Detection</h1>
        <p>Advanced deepfake detection powered by AI</p>
      </div>
      
      <div className="upload-section">
        <div className="file-input-wrapper">
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleImageUpload}
            id="file-input"
            className="file-input"
          />
          <label htmlFor="file-input" className="file-label">
            <FiFolder />
            Choose Image
          </label>
        </div>
        
        {image && (
          <div className="image-preview">
            <img src={image} alt="Preview" className="preview-img" />
            <button 
              onClick={uploadImage} 
              disabled={loading}
              className="upload-btn"
            >
              {loading ? (
                <>
                  <FiLoader className="spinning" />
                  Analyzing...
                </>
              ) : (
                <>
                  <FiEye />
                  Analyze
                </>
              )}
            </button>
          </div>
        )}
      </div>
      
      {error && (
        <div className="alert error">
          <FiX />
          <span>{error}</span>
        </div>
      )}
      
      {result && result.body?.detection_result && (
        <div className="results-section">
          <div className="results-header">
            <FiEye className="results-icon" />
            <h3>Analysis Complete</h3>
          </div>
          
          {result.body.detection_result.data[0].bounding_boxes.map((detection, i) => {
            const isDeepfake = detection.is_deepfake > 0.5
            const fakeConfidence = (detection.is_deepfake * 100).toFixed(1)
            const realConfidence = ((1 - detection.is_deepfake) * 100).toFixed(1)
            const detectionConf = (detection.bbox_confidence * 100).toFixed(1)
            
            return (
              <div key={i} className={`result-card ${isDeepfake ? 'fake' : 'real'}`}>
                <div className="result-main">
                  <div className="result-icon">
                    {isDeepfake ? <FiX size={24} /> : <FiCheck size={24} />}
                  </div>
                  <div className="result-content">
                    <div className="status-badge">
                      {isDeepfake ? 'DEEPFAKE DETECTED' : 'AUTHENTIC IMAGE'}
                    </div>
                    <div className="confidence-score">
                      {isDeepfake ? 'Fake' : 'Authentic'} Confidence: <strong>{isDeepfake ? fakeConfidence : realConfidence}%</strong>
                    </div>
                    <div className="detection-score">
                      Detection Accuracy: <strong>{detectionConf}%</strong>
                    </div>
                  </div>
                </div>
                <div className="confidence-bar">
                  <div 
                    className={`confidence-fill ${isDeepfake ? 'fake-fill' : 'real-fill'}`}
                    style={{ width: `${isDeepfake ? fakeConfidence : realConfidence}%` }}
                  ></div>
                </div>
              </div>
            )
          })}
        </div>
      )}
      
      <footer style={{ 
        textAlign: 'center', 
        marginTop: '2rem', 
        padding: '1rem', 
        fontSize: '0.8rem', 
        opacity: '0.7',
        color: 'white'
      }}>
        Built by Louis Echefu
      </footer>
    </div>
  )
}

export default App