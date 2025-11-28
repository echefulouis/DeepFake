import { FiCheck, FiX, FiEye } from 'react-icons/fi'

const ResultDisplay = ({ result, image }) => {
  if (!result || !result.detection_result) return null

  const detections = result.detection_result.data[0].bounding_boxes

  return (
    <div className="results-container">
      <h3>Detection Results</h3>
      
      <div className="image-with-boxes">
        <canvas 
          id="result-canvas"
          style={{ maxWidth: '100%', border: '1px solid #ddd', borderRadius: '8px' }}
        />
      </div>

      <div className="detection-cards">
        {detections.map((detection, i) => (
          <div 
            key={i} 
            className={`detection-card ${detection.is_deepfake > 0.5 ? 'fake' : 'real'}`}
          >
            <div className="detection-header">
              {detection.is_deepfake > 0.5 ? <FiX /> : <FiCheck />}
              <span className="status">
                {detection.is_deepfake > 0.5 ? 'DEEPFAKE' : 'AUTHENTIC'}
              </span>
              <span className="confidence">
                {(detection.is_deepfake * 100).toFixed(1)}%
              </span>
            </div>
            <p className="bbox-confidence">
              Detection Confidence: {(detection.bbox_confidence * 100).toFixed(1)}%
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ResultDisplay