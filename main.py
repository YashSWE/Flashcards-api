from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from google import genai
from google.genai import types

app = FastAPI()

# CORS setup (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class CardRequest(BaseModel):
    topic: str
    cardCount: int
    field1Label: str
    field2Label: str
    field3Label: Optional[str] = None
    field4Label: Optional[str] = None
    template: str
    systemPrompt: Optional[str] = None

class Card(BaseModel):
    field1: str
    field2: str
    field3: Optional[str] = None
    field4: Optional[str] = None


# --- Google GenAI SDK setup ---
# Set GEMINI_API_KEY in your environment or pass explicitly below
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else genai.Client()


@app.post("/api/generate-cards", response_model=List[Card])
def generate_cards(req: CardRequest):
    # Build prompt
    prompt = f"Generate {req.cardCount} flashcards about '{req.topic}'.\n"
    prompt += f"For each flashcard, create the following fields:\n1. {req.field1Label}\n2. {req.field2Label}"
    if req.template != '2-field':
        prompt += f"\n3. {req.field3Label}"
    if req.template == '4-field':
        prompt += f"\n4. {req.field4Label}"
    if req.systemPrompt:
        prompt += f"\n\nAdditional instructions: {req.systemPrompt}"
    prompt += ("\n\nReturn the response as a JSON array where each object has the fields: field1, field2"
               f"{', field3' if req.template != '2-field' else ''}{', field4' if req.template == '4-field' else ''}.")
    prompt += "\nMake sure to return ONLY the JSON array, no additional text."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # or another Gemini model name
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=2000,
            ),
        )
        # The SDK will parse JSON if possible
        cards = response.parsed if hasattr(response, "parsed") and response.parsed else None
        if cards is None:
            import json
            import re
            text = response.text.strip()
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                cards = json.loads(match.group(0))
            else:
                raise HTTPException(status_code=500, detail="AI did not return valid JSON.")
        sanitized = []
        for card in cards[:req.cardCount]:
            sanitized.append({
                "field1": card.get("field1", ""),
                "field2": card.get("field2", ""),
                "field3": card.get("field3", "") if req.template != '2-field' else None,
                "field4": card.get("field4", "") if req.template == '4-field' else None,
            })
        return sanitized
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health():
    return {"status": "ok"}
