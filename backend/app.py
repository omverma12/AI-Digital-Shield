from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI Digital Shield")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "AI Digital Shield is running"
    }


@app.post("/analyze")
def analyze_message(request: MessageRequest):

    message = request.message.lower()

    risk_score = 0
    reasons = []

    # Urgency detection
    urgency_words = [
        "urgent",
        "immediately",
        "within",
        "limited time",
        "30 minutes",
        "24 hours",
        "expire",
        "blocked"
    ]

    for word in urgency_words:
        if word in message:
            risk_score += 25
            reasons.append("Artificial urgency detected")
            break

    # Sensitive information detection
    sensitive_words = [
        "aadhaar",
        "pan",
        "otp",
        "password",
        "bank details",
        "card number",
        "cvv"
    ]

    for word in sensitive_words:
        if word in message:
            risk_score += 30
            reasons.append("Sensitive information requested")
            break

    # Link detection
    if (
        "http://" in message
        or "https://" in message
        or "click here" in message
    ):
        risk_score += 30
        reasons.append("Suspicious link or call-to-action detected")

    # Scam pattern detection
    scam_words = [
        "verify your account",
        "account suspended",
        "prize",
        "lottery",
        "won",
        "refund",
        "kyc"
    ]

    for word in scam_words:
        if word in message:
            risk_score += 20
            reasons.append("Common scam/phishing pattern detected")
            break

    risk_score = min(risk_score, 100)

    if risk_score >= 60:

        risk_level = "HIGH"

        action = (
            "Do not click links or share sensitive information. "
            "Verify through the official source."
        )

    elif risk_score >= 30:

        risk_level = "MEDIUM"

        action = (
            "Be cautious. Verify the sender and information "
            "before taking any action."
        )

    else:

        risk_level = "LOW"

        action = (
            "No major suspicious patterns detected. "
            "Still verify unexpected requests."
        )

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "reasons": reasons,
        "recommended_action": action
    }