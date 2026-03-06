from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

spamWords = {
  "urgent": 2.5,
  "immediately": 2.0,
  "act": 1.5,
  "now": 1.25,
  "limited": 1.5,
  "expires": 1.75,
  "today": 1.0,
  "final": 1.25,
  "last": 1.0,
  "hurry": 2.0,
  "free": 2.0,
  "winner": 3.0,
  "won": 2.5,
  "prize": 2.5,
  "jackpot": 3.0,
  "reward": 2.0,
  "cash": 2.0,
  "bonus": 2.0,
  "gift": 1.75,
  "giveaway": 2.25,
  "voucher": 1.75,
  "credit": 1.5,
  "loan": 2.0,
  "debt": 1.75,
  "mortgage": 1.25,
  "refinance": 1.75,
  "investment": 1.25,
  "crypto": 2.25,
  "bitcoin": 2.5,
  "profit": 2.0,
  "earn": 2.0,
  "income": 1.75,
  "rich": 2.5,
  "million": 2.0,
  "verify": 2.5,
  "verification": 2.5,
  "confirm": 2.0,
  "login": 1.75,
  "password": 2.5,
  "account": 1.75,
  "suspended": 3.0,
  "locked": 2.5,
  "unauthorized": 2.0,
  "security": 1.5,
  "alert": 1.75,
  "notice": 1.25,
  "click": 2.25,
  "link": 1.5,
  "open": 1.25,
  "download": 2.0,
  "install": 2.0,
  "subscribe": 1.5,
  "unsubscribe": 1.25,
  "deal": 1.5,
  "sale": 1.25,
  "discount": 1.75,
  "offer": 1.5,
  "promo": 1.75,
  "promotion": 1.5,
  "bargain": 1.5,
  "buy": 1.25,
  "order": 1.25,
  "viagra": 4.0,
  "cialis": 4.0,
  "pharmacy": 3.0,
  "pills": 3.0,
  "guarantee": 2.25,
  "guaranteed": 2.25,
  "no": 0.1,
  "risk-free": 2.25,
  "trial": 1.25,
  "miracle": 3.0,
  "no strings": 2.0,
  "no fees": 2.0,
  "no cost": 2.0,
  "work from home": 2.5,
  "make money": 2.5,
  "easy money": 3.0,
  "get paid": 2.25,
  "dear": 1.25,
  "customer": 1.5,
  "valued": 1.25,
  "user": 1.0,
  "member": 1.0,
  "giftcard": 3.25,
  "gift-card": 3.25,
  "itunes": 3.0,
  "steam": 2.25,
  "paypal": 2.0,
  "venmo": 1.75,
  "zelle": 2.5,
  "wire": 2.5,
  "transfer": 1.75
}
numbers = [
  "1",
  "2",
  "3",
  "4",
  "5",
  "6",
  "7",
  "8",
  "9",
  "0",
]
letters = [
 "a",
 "b",
 "c",
 "d",
 "e",
 "f",
 "g",
 "h",
 "i",
 "j",
 "k",
 "l",
 "m",
 "n",
 "o",
 "p",
 "q",
 "r",
 "s",
 "t",
 "u",
 "v",
 "w",
 "x",
 "y",
 "z"
]

def calculate_risk(subject, message):
    subjectWords = []
    messageWords = []
    risk = 0
    build = ""
    for char in message:
      if char.lower() in letters:
        build = f"{build}{char}"
      elif char in numbers:
        build = f"{build}{char}"
        risk += .25
      elif char != " " and char != "\n" and char != ",":
        build = f"{build}{char}"
        risk += 1
      else:
        if build:
            messageWords.append(build)
        build = ""
    if build:
        messageWords.append(build)
    
    build = ""
    for char in subject:
      if char.lower() in letters:
        build = f"{build}{char}"
      elif char in numbers:
        build = f"{build}{char}"
        risk += .25
      elif char != " " and char != "," and char != ".":
        build = f"{build}{char}"
        risk += 1
      else:
        if build:
            subjectWords.append(build)
        build = ""
    if build:
        subjectWords.append(build)
    
    for word, wordRisk in spamWords.items():
      risk += wordRisk * message.lower().count(word.lower()) / max(1, (len(message) / 2.5))
      risk += wordRisk * subject.lower().count(word.lower())
    
    return risk

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    subject = data.get('subject', '')
    message = data.get('message', '')
    leniency = data.get('leniency', 3)  # Default to 3 (medium)
    
    # Convert leniency (1-5 scale) to threshold
    # 1 = strict (threshold 20), 3 = medium (threshold 15), 5 = lenient (threshold 5)
    threshold = 20 - (leniency - 1) * 3.75
    
    risk = calculate_risk(subject, message)
    is_spam = risk >= threshold
    print(f"Subject: {subject[:50]}... | Risk: {risk:.2f} | Threshold: {threshold:.2f} | Spam: {is_spam}")
    return jsonify({'risk': risk, 'is_spam': is_spam})

if __name__ == '__main__':
    app.run(debug=True)