import requests
import json

# Test legitimate emails
legitimate_emails = [
    {
        "subject": "Team meeting tomorrow at 2pm",
        "message": "Hi, just confirming our meeting is still on for tomorrow at 2pm in the conference room. Please let me know if you need anything."
    },
    {
        "subject": "Project update",
        "message": "Here's the latest status on the Q1 project. We've completed the design phase and are moving into development. Timeline is on track."
    },
    {
        "subject": "Lunch plans?",
        "message": "Want to grab lunch together next Tuesday? I'm thinking that new Italian place downtown."
    },
    {
        "subject": "Document attached",
        "message": "I've attached the quarterly report you requested. Let me know if you have any questions about the numbers."
    },
    {
        "subject": "Happy Birthday!",
        "message": "Hope you have a wonderful birthday! Let's celebrate this weekend."
    },
]

# Test spam emails
spam_emails = [
    {
        "subject": "URGENT: Verify your account NOW!",
        "message": "Click the link immediately to verify your account before it gets suspended. This is a final notice. Act now or lose access forever!"
    },
    {
        "subject": "Congratulations! You won a prize!",
        "message": "You've won a jackpot! Claim your cash reward today. Limited time offer expires today. Click here now to claim your prize!"
    },
    {
        "subject": "Make money fast from home",
        "message": "Earn easy money working from home. Make $5000 per week guaranteed! No experience needed. Click to get started now!"
    },
    {
        "subject": "Free gift card inside",
        "message": "Claim your free iTunes gift card now! This offer is for you, valued customer. Download and verify to receive your reward immediately."
    },
    {
        "subject": "Your PayPal account requires verification",
        "message": "URGENT: Verify your PayPal login and password immediately. Unauthorized access has been detected. Confirm your account now!"
    },
]

API_URL = "http://localhost:5000/analyze"

print("=" * 80)
print("LEGITIMATE EMAILS")
print("=" * 80)
legit_scores = []
for i, email in enumerate(legitimate_emails, 1):
    try:
        response = requests.post(API_URL, json=email)
        data = response.json()
        risk = data['risk']
        legit_scores.append(risk)
        print(f"{i}. Risk: {risk:.2f} | Is Spam: {data['is_spam']}")
        print(f"   Subject: {email['subject']}\n")
    except Exception as e:
        print(f"Error testing email {i}: {e}\n")

print("\n" + "=" * 80)
print("SPAM EMAILS")
print("=" * 80)
spam_scores = []
for i, email in enumerate(spam_emails, 1):
    try:
        response = requests.post(API_URL, json=email)
        data = response.json()
        risk = data['risk']
        spam_scores.append(risk)
        print(f"{i}. Risk: {risk:.2f} | Is Spam: {data['is_spam']}")
        print(f"   Subject: {email['subject']}\n")
    except Exception as e:
        print(f"Error testing email {i}: {e}\n")

print("\n" + "=" * 80)
print("SUMMARY STATISTICS")
print("=" * 80)
if legit_scores:
    print(f"Legitimate emails:")
    print(f"  Min: {min(legit_scores):.2f}")
    print(f"  Max: {max(legit_scores):.2f}")
    print(f"  Avg: {sum(legit_scores)/len(legit_scores):.2f}")

if spam_scores:
    print(f"Spam emails:")
    print(f"  Min: {min(spam_scores):.2f}")
    print(f"  Max: {max(spam_scores):.2f}")
    print(f"  Avg: {sum(spam_scores)/len(spam_scores):.2f}")

print("\n" + "=" * 80)
if legit_scores and spam_scores:
    max_legit = max(legit_scores)
    min_spam = min(spam_scores)
    print(f"Legitimate max: {max_legit:.2f}")
    print(f"Spam min: {min_spam:.2f}")
    if max_legit < min_spam:
        print(f"Suggested threshold: {(max_legit + min_spam) / 2:.2f}")
    else:
        print(f"Warning: Scores overlap! Consider reviewing the scoring algorithm.")
