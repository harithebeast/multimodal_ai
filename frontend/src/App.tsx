import { useState, useRef } from 'react';
import { LiveKitRoom, VideoConference } from '@livekit/components-react';
import '@livekit/components-styles';
import './App.css';

function App() {
  const [token, setToken] = useState<string>('');
  const [url, setUrl] = useState<string>('');
  const [participantName, setParticipantName] = useState<string>('');
  const [connected, setConnected] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string>('');
  const [annotatedImage, setAnnotatedImage] = useState<string>('');
  const [detectionResult, setDetectionResult] = useState<string>('');
  const [parsedAnalysis, setParsedAnalysis] = useState<any>(null);
  const [detections, setDetections] = useState<any[]>([]);
  const [structuredData, setStructuredData] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Parse LLM output to extract structured sections
  const parseLLMOutput = (text: string) => {
    const sections: any = {
      confirmed: [],
      notVisible: [],
      notes: []
    };

    // Split by lines and process
    const lines = text.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      
      // Skip empty lines and emoji-only lines
      if (!trimmed || trimmed.match(/^[🔍📋✅⚠️📝]+$/)) continue;

      // Parse bullet points with * (single star)
      if (trimmed.startsWith('*')) {
        const content = trimmed.substring(1).trim();
        
        // Check if it's a component description with colon
        if (content.includes(':')) {
          // Extract component name (may have **bold**)
          const colonIndex = content.indexOf(':');
          let componentPart = content.substring(0, colonIndex).trim();
          let statusPart = content.substring(colonIndex + 1).trim();
          
          // Remove markdown bold markers
          componentPart = componentPart.replace(/\*\*/g, '');
          statusPart = statusPart.replace(/\*\*/g, '');
          
          const componentName = componentPart;
          const statusText = statusPart;
          
          // Categorize based on status text
          const statusLower = statusText.toLowerCase();
          
          if (statusLower.includes('confirmed')) {
            sections.confirmed.push({ name: componentName, status: statusText });
          } else if (
            statusLower.includes('not visible') || 
            statusLower.includes('not explicitly visible') ||
            statusLower.includes('obscured') ||
            statusLower.includes('not detected') ||
            statusLower.includes('likely present')
          ) {
            sections.notVisible.push({ name: componentName, status: statusText });
          } else {
            sections.notes.push({ name: componentName, status: statusText });
          }
        }
      }
    }

    return sections;
  };

  const connect = async () => {
    if (!participantName) {
      alert('Participant name is required');
      return;
    }

    try {
      const response = await fetch(`http://localhost:8000/api/get-token?participant=${encodeURIComponent(participantName)}`);
      const data = await response.json();
      setToken(data.token);
      setUrl(data.url);
      setConnected(true);
    } catch (e) {
      console.error(e);
      alert('Failed to get token. Please check console for details.');
    }
  };

  const onConnected = () => {
    setConnected(true);
    console.log('Connected to room');
  }

  const onDisconnected = () => {
    setConnected(false);
    setToken('');
    console.log('Disconnected from room');
  };

  const onError = (error: Error) => {
    console.error('Error:', error);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
      }
      setSelectedImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      setDetectionResult('');
    }
  };

  const handleImageUpload = async () => {
    if (!selectedImage) {
      alert('Please select an image first');
      return;
    }

    setIsAnalyzing(true);
    setDetectionResult('');

    try {
      const formData = new FormData();
      formData.append('image', selectedImage);

      const response = await fetch('http://localhost:8000/api/detect-component', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      setDetectionResult(data.analysis);
      setDetections(data.detections || []);
      setStructuredData(data.structured_data || null);
      
      // Parse the analysis text for better display
      if (data.analysis) {
        const parsed = parseLLMOutput(data.analysis);
        setParsedAnalysis(parsed);
      }
      
      // Display annotated image with bounding boxes if available
      if (data.annotated_image) {
        setAnnotatedImage(data.annotated_image);
      }
    } catch (error) {
      console.error('Error analyzing image:', error);
      alert('Failed to analyze image. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
    setImagePreview('');
    setAnnotatedImage('');
    setDetectionResult('');
    setDetections([]);
    setStructuredData(null);
    setParsedAnalysis(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="container" data-lk-theme="default">
      <h1>Hardware Assistant AI</h1>
      
      {!connected ? (
        <div className="card">
          <h2>Join Room</h2>
          <div className="form-group">
            <label htmlFor="participant">Your Name:</label>
            <input
              id="participant"
              type="text"
              value={participantName}
              onChange={(e) => setParticipantName(e.target.value)}
              placeholder="Enter your name"
            />
          </div>
          <button onClick={connect}>Connect</button>
        </div>
      ) : (
        <>
          <div className="video-container">
            <LiveKitRoom
              serverUrl={url}
              token={token}
              connect={true}
              onConnected={onConnected}
              onDisconnected={onDisconnected}
              onError={onError}
              audio={true}
              video={true}
            >
              <VideoConference />
            </LiveKitRoom>
          </div>

          <div className="card image-upload-card">
            <h2>Upload Component Image for Analysis</h2>
            <div className="image-upload-section">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleImageSelect}
                style={{ display: 'none' }}
                id="image-upload"
              />
              <label htmlFor="image-upload" className="upload-button">
                📷 Choose Component Image
              </label>

              {imagePreview && (
                <div className="image-preview-container">
                  <img 
                    src={annotatedImage || imagePreview} 
                    alt="Preview" 
                    className="image-preview" 
                  />
                  {detections.length > 0 && (
                    <div className="detections-legend">
                      <strong>Detected Components:</strong>
                      <ul>
                        {detections.map((det, idx) => (
                          <li key={idx}>
                            {det.class} - {(det.confidence * 100).toFixed(1)}% confidence
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div className="image-actions">
                    <button onClick={handleImageUpload} disabled={isAnalyzing}>
                      {isAnalyzing ? '🔍 Analyzing...' : '🔍 Detect Component'}
                    </button>
                    <button onClick={clearImage} className="clear-button">❌ Clear</button>
                  </div>
                </div>
              )}

              {detectionResult && parsedAnalysis && (
                <div className="analysis-container">
                  {/* Annotated Image */}
                  {annotatedImage && (
                    <div className="dark-card annotated-image-card">
                      <h3 className="card-title">📸 Component Analysis</h3>
                      <img 
                        src={annotatedImage} 
                        alt="Analyzed components" 
                        className="analyzed-image"
                      />
                    </div>
                  )}

                  {/* Component Grid - Square Cards */}
                  <div className="dark-card components-grid-card">
                    <h3 className="card-title">🔍 Detected Components</h3>
                    
                    <div className="components-grid">
                      {/* Confirmed Components */}
                      {parsedAnalysis.confirmed && parsedAnalysis.confirmed.map((item: any, idx: number) => (
                        <div key={`confirmed-${idx}`} className="component-square confirmed">
                          <div className="square-icon">✓</div>
                          <div className="square-name">{item.name}</div>
                          <div className="square-status">Confirmed</div>
                        </div>
                      ))}

                      {/* Not Visible / Obscured */}
                      {parsedAnalysis.notVisible && parsedAnalysis.notVisible.map((item: any, idx: number) => (
                        <div key={`not-visible-${idx}`} className="component-square not-visible">
                          <div className="square-icon">⚠</div>
                          <div className="square-name">{item.name}</div>
                          <div className="square-status">Not Visible</div>
                        </div>
                      ))}

                      {/* Notes */}
                      {parsedAnalysis.notes && parsedAnalysis.notes.map((item: any, idx: number) => (
                        <div key={`notes-${idx}`} className="component-square notes">
                          <div className="square-icon">📝</div>
                          <div className="square-name">{item.name}</div>
                          <div className="square-status">Note</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Raw Analysis Dropdown */}
                  <div className="dark-card raw-analysis">
                    <details>
                      <summary className="dropdown-toggle">
                        <span>📄 View Raw Analysis</span>
                        <span className="dropdown-arrow">▼</span>
                      </summary>
                      <div className="dropdown-content">
                        <p className="raw-text">{detectionResult}</p>
                      </div>
                    </details>
                  </div>
                </div>
              )}

              {!parsedAnalysis && detectionResult && (
                <div className="detection-result">
                  <h3>✅ Analysis Result:</h3>
                  <p>{detectionResult}</p>
                </div>
              )}

              {structuredData && structuredData.recommendations && structuredData.recommendations.length > 0 && (
                <div className="dark-card upgrade-instructions-card">
                  <h3 className="card-title">📋 Upgrade Instructions</h3>
                  {structuredData.recommendations.map((rec: any, idx: number) => (
                    <details key={idx} className="upgrade-dropdown">
                      <summary className="dropdown-toggle">
                        <span className="upgrade-component-name">{rec.component}</span>
                        <span className="dropdown-arrow">▼</span>
                      </summary>
                      <div className="dropdown-content">
                        <p className="upgrade-message">{rec.message}</p>
                        {rec.next_steps && rec.next_steps.length > 0 && (
                          <div className="next-steps-list">
                            <strong>Next Steps:</strong>
                            <ol>
                              {rec.next_steps.map((step: string, stepIdx: number) => (
                                <li key={stepIdx}>{step}</li>
                              ))}
                            </ol>
                          </div>
                        )}
                      </div>
                    </details>
                  ))}
                  <div className="upgrade-summary">
                    <strong>📊 Summary:</strong> {structuredData.summary}
                  </div>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
