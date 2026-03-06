// Initialize settings on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeTheme();
  initializeLeniency();
  setupEventListeners();
});

// ============= Theme Management =============
function initializeTheme() {
  chrome.storage.sync.get(['theme'], (result) => {
    const savedTheme = result.theme || 'system';
    const themeSelect = document.getElementById('themeToggle');
    themeSelect.value = savedTheme;
    applyTheme(savedTheme);
  });
}

function applyTheme(theme) {
  const html = document.documentElement;
  
  if (theme === 'system') {
    // Check browser preference
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    html.classList.toggle('dark-mode', prefersDark);
  } else if (theme === 'dark') {
    html.classList.add('dark-mode');
  } else {
    html.classList.remove('dark-mode');
  }
}

document.getElementById('themeToggle').addEventListener('change', (e) => {
  const theme = e.target.value;
  chrome.storage.sync.set({ theme });
  applyTheme(theme);
});

// Listen for system theme changes
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  chrome.storage.sync.get(['theme'], (result) => {
    if (result.theme === 'system') {
      applyTheme('system');
    }
  });
});

// ============= Leniency Management =============
function initializeLeniency() {
  chrome.storage.sync.get(['leniency'], (result) => {
    const leniency = result.leniency || 3;
    document.getElementById('leniency').value = leniency;
  });
}

document.getElementById('leniency').addEventListener('change', (e) => {
  chrome.storage.sync.set({ leniency: parseInt(e.target.value) });
});

// ============= Settings Modal =============
function setupEventListeners() {
  const settingsBtn = document.getElementById('settingsBtn');
  const settingsModal = document.getElementById('settingsModal');
  const closeSettingsBtn = document.getElementById('closeSettingsBtn');

  settingsBtn.addEventListener('click', () => {
    settingsModal.classList.remove('hidden');
  });

  closeSettingsBtn.addEventListener('click', () => {
    settingsModal.classList.add('hidden');
  });

  // Close modal when clicking outside the panel
  settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
      settingsModal.classList.add('hidden');
    }
  });
}

// ============= Spam Analysis =============
document.getElementById('analyze').addEventListener('click', async () => {
  const subject = document.getElementById('subject').value;
  const message = document.getElementById('message').value;

  if (!subject && !message) {
    showResult('Please enter subject or message', 'safe');
    return;
  }

  // Get leniency setting
  chrome.storage.sync.get(['leniency'], async (result) => {
    const leniency = result.leniency || 3;

    try {
      const response = await fetch('https://congenial-meme-r46qpr95wwgxh5gqj-5000.app.github.dev/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ subject, message, leniency })
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
});

function showResult(text, type) {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = text;
  resultDiv.className = `result ${type}`;
}