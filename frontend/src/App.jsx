import { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [steps, setSteps] = useState(50);
  const [scale, setScale] = useState(7.5);
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setImageUrl('');
    try {
      const response = await axios.post('http://localhost:8000/generate', {
        prompt,
        steps: Number(steps),
        scale: Number(scale)
      });
      setImageUrl('http://localhost:8000' + response.data.url);
    } catch (err) {
      alert('Error generating image');
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6">Custom Text-to-Image Generator</h1>

      <input
        type="text"
        className="w-full max-w-lg p-3 rounded text-black mb-2"
        placeholder="Enter your prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />

      <div className="flex gap-4 mb-2">
        <input
          type="number"
          className="p-2 rounded text-black"
          placeholder="Steps"
          value={steps}
          onChange={(e) => setSteps(e.target.value)}
        />
        <input
          type="number"
          step="0.1"
          className="p-2 rounded text-black"
          placeholder="Scale"
          value={scale}
          onChange={(e) => setScale(e.target.value)}
        />
      </div>

      <button
        onClick={handleGenerate}
        className="bg-blue-500 hover:bg-blue-600 mt-2 px-6 py-2 rounded text-white font-semibold"
        disabled={loading}
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {imageUrl && (
        <img src={imageUrl} alt="Generated" className="mt-6 max-w-xl rounded shadow-xl" />
      )}
    </div>
  );
}

export default App;
