![Spamshield logo](https://videos.openai.com/az/vg-assets/task_01kk0f7g9zfck8bw8fm4s53750%2F1772763754_img_0.webp?se=2026-03-08T00%3A00%3A00Z&sp=r&sv=2026-02-06&sr=b&skoid=aa5ddad1-c91a-4f0a-9aca-e20682cc8969&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2026-03-05T12%3A59%3A29Z&ske=2026-03-12T13%3A04%3A29Z&sks=b&skv=2026-02-06&sig=Cf8CHesl3jiWMfcbJcYrHXDvM35XRK4dTmXTEHqnIo8%3D&ac=oaivgprodscus2)

A browser extension that helps detect spam emails by analyzing subject and message content using a custom algorithm.

## Features

- Manual analysis: Enter email subject and body in the extension popup
- Automated analysis: On supported webmail sites (Gmail, Outlook, Yahoo), a "Check Spam" button appears next to the email subject
- Backend API for spam detection

## Installation

1. Clone or download this repository
2. Install the extension in your browser:
   - For Chrome: Go to `chrome://extensions/`, enable "Developer mode", click "Load unpacked", select the SpamShield folder
   - For Firefox: Go to `about:debugging`, click "This Firefox", click "Load Temporary Add-on", select `manifest.json`
3. Start the backend server: `python backend.py`
4. The extension should now be active

## Usage

### Manual Analysis
1. Click the SpamShield icon in your browser toolbar
2. Enter the email subject and message
3. Click "Analyze Spam"
4. View the result

### Automated Analysis
1. Open an email on Gmail, Outlook, or Yahoo Mail
2. Look for the "Check Spam" button next to the subject
3. Click it to analyze the email
4. View the result in an alert

## Backend API

The backend runs on `http://localhost:5000/analyze` and accepts POST requests with JSON:

```json
{
  "subject": "Email subject",
  "message": "Email body"
}
```

Response:

```json
{
  "risk": 25.5,
  "is_spam": false
}
```

## Algorithm

The spam detection algorithm calculates a risk score based on:
- Presence of spam keywords with weighted scores
- Number of numbers and symbols in the text
- Length of the message

Emails with risk >= 30 are considered spam.

## Supported Sites

- Gmail (mail.google.com)
- Outlook (outlook.live.com)
- Yahoo Mail (mail.yahoo.com)

## Requirements

- Python 3.x
- Flask (`pip install flask`)
- Modern web browser with extension support

if you have any problems using SpamShield, [write an issue](https://github.com/DaYoungMythic/SpamShield/issues/new/choose)