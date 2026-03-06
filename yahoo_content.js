// Yahoo content script for SpamShield

function extractEmailData() {
  const subjectElement = document.querySelector('h1[data-test-id="message-view-subject"]');
  const bodyElement = document.querySelector('div[data-test-id="message-view-body-content"]');
  
  if (!subjectElement || !bodyElement) {
    return null;
  }
  
  const subject = subjectElement.textContent.trim();
  const message = bodyElement.textContent.trim();
  
  return { subject, message };
}

function addSpamCheckButton() {
  const subjectElement = document.querySelector('h1[data-test-id="message-view-subject"]');
  if (!subjectElement) return;
  
  // Check if button already exists
  if (document.getElementById('spamshield-button')) return;
  
  const button = document.createElement('button');
  button.id = 'spamshield-button';
  button.textContent = 'Check Spam';
  button.style.marginLeft = '10px';
  button.style.padding = '5px 10px';
  button.style.backgroundColor = '#007bff';
  button.style.color = 'white';
  button.style.border = 'none';
  button.style.borderRadius = '4px';
  button.style.cursor = 'pointer';
  
  button.addEventListener('click', async () => {
    const data = extractEmailData();
    if (!data) {
      alert('Could not extract email data');
      return;
    }
    
    button.textContent = 'Analyzing...';
    button.disabled = true;
    
    try {
      const response = await fetch('https://congenial-meme-r46qpr95wwgxh5gqj-5000.app.github.dev/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      const result = await response.json();
      const resultText = result.is_spam ? `SPAM! Risk: ${result.risk.toFixed(2)}` : `Safe. Risk: ${result.risk.toFixed(2)}`;
      alert(`SpamShield Result: ${resultText}`);
    } catch (error) {
      alert('Error connecting to SpamShield backend');
    } finally {
      button.textContent = 'Check Spam';
      button.disabled = false;
    }
  });
  
  subjectElement.parentNode.insertBefore(button, subjectElement.nextSibling);
}

// Wait for the page to load and add the button
const observer = new MutationObserver(() => {
  if (document.querySelector('h1[data-test-id="message-view-subject"]')) {
    addSpamCheckButton();
  }
});

observer.observe(document.body, { childList: true, subtree: true });

// Also check immediately
addSpamCheckButton();