# Flashcards FastAPI Backend – API Documentation

## Overview
This backend provides endpoints for generating flashcards using the Gemini LLM (via Google GenAI SDK).

---

## Base URL
- When running locally: `http://localhost:10000`
- When deployed on Render: `https://<your-app-name>.onrender.com`

---

## Endpoints

### 1. Health Check
- **GET** `/api/health`
- **Description:** Returns a simple status message to verify the API is running.
- **Response:**
  ```json
  { "status": "ok" }
  ```

---

### 2. Generate Flashcards
- **POST** `/api/generate-cards`
- **Description:** Generate flashcards for a given topic and template using Gemini LLM.
- **Request Body:**
  ```json
  {
    "topic": "string",
    "cardCount": 20,
    "field1Label": "string",
    "field2Label": "string",
    "field3Label": "string (optional)",
    "field4Label": "string (optional)",
    "template": "2-field" | "3-field" | "4-field",
    "systemPrompt": "string (optional)"
  }
  ```
- **Response:**
  ```json
  [
    {
      "field1": "...",
      "field2": "...",
      "field3": "...", // optional
      "field4": "..."  // optional
    },
    ...
  ]
  ```
- **Notes:**
  - The number of cards returned will not exceed `cardCount`.
  - The fields returned depend on the selected template.

---

## Example Usage

### Health Check
```bash
curl https://<your-app-name>.onrender.com/api/health
```

### Generate Cards
```bash
curl -X POST https://<your-app-name>.onrender.com/api/generate-cards \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Photosynthesis",
    "cardCount": 5,
    "field1Label": "Question",
    "field2Label": "Answer",
    "template": "2-field"
  }'
```

---

## Environment Variables
- `GEMINI_API_KEY`: Your Gemini API key (must be set in the Render dashboard or `.env` file for local development).

---

## Contact
- Maintainer: YashSWE
- For issues, open a GitHub issue or contact the maintainer.
