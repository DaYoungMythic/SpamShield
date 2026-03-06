document.getElementById('analyze').addEventListener('click', async () => {
  const subject = document.getElementById('subject').value;
  const message = document.getElementById('message').value;
  
  if (!subject && !message) {
    showResult('Please enter subject or message', 'safe');
    return;
  }
  
  try {
    const response = await fetch('http://localhost:5000/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ subject, message })
    });
    
    if (!response.ok) {
      throw new Error('Failed to analyze');
    }
    
    const data = await response.json();
    const resultText = data.is_spam ? `SPAM DETECTED! Risk: ${data.risk.toFixed(2)}` : `Safe. Risk: ${data.risk.toFixed(2)}`;
    showResult(resultText, data.is_spam ? 'spam' : 'safe');
  } catch (error) {
    showResult('Error: Could not connect to backend. Make sure the server is running.', 'safe');
  }
});

function showResult(text, type) {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = text;
  resultDiv.className = `result ${type}`;
}