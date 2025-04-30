from fastapi import FastAPI, Form
import requests

app = FastAPI()

@app.post("/analyze/")
def analyze_sentiment(text: str = Form(...)):
    """
    Receives text input, sends it to the Ollama Mistral model for sentiment analysis,
    and returns the predicted sentiment.
    """
    prompt = f"What is the sentiment of this text? Respond with Positive, Negative, or Neutral:\n\n{text}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=20  # Add a timeout
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
        # Basic cleaning of the response
        sentiment = result.get("response", "").strip().capitalize()
        # Ensure only valid responses are returned
        if sentiment in ["Positive", "Negative", "Neutral"]:
            return {"sentiment": sentiment}
        else:
            # Fallback or logging if the response is not as expected
            print(f"Unexpected response from model: {sentiment}")
            return {"sentiment": "Error: Unexpected response from model"}
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return {"sentiment": f"Error: Could not connect to Ollama - {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"sentiment": f"Error: An unexpected error occurred - {e}"}

# Optional: Add a root endpoint for basic check
@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis Backend is running!"} 