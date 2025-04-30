import streamlit as st
import requests

st.set_page_config(layout="wide") # Use wide layout for better spacing

st.title("📝 Sentiment Analyzer (Mistral)")
st.caption("Powered by Ollama Mistral & FastAPI")

# Backend API URL
BACKEND_URL = "http://localhost:8000/analyze/"

# Input area
text_input = st.text_area("Enter text to analyze:", height=150, placeholder="Type or paste your text here...")

# Analyze button
if st.button("Analyze Sentiment", type="primary"):
    if text_input:
        try:
            # Show a spinner while processing
            with st.spinner('Analyzing...'):
                # Send request to backend
                response = requests.post(BACKEND_URL, data={"text": text_input}, timeout=25)
                response.raise_for_status() # Check for HTTP errors
                
            # Parse the response
            result = response.json()
            sentiment = result.get("sentiment", "Error: Could not parse sentiment")

            # Display result
            st.subheader("Predicted Sentiment:")
            if "Error:" in sentiment:
                st.error(sentiment)
            elif sentiment == "Positive":
                st.success(f"**{sentiment}** 😊")
            elif sentiment == "Negative":
                st.warning(f"**{sentiment}** 😠")
            elif sentiment == "Neutral":
                st.info(f"**{sentiment}** 😐")
            else:
                 st.write(sentiment) # Fallback for unexpected valid sentiment

        except requests.exceptions.ConnectionError:
            st.error("Error: Could not connect to the backend. Is it running?")
        except requests.exceptions.Timeout:
             st.error("Error: The request to the backend timed out.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error during analysis: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please enter some text to analyze.")

# Add some instructions or info
st.divider()
st.markdown("**How it works:** This app sends your text to a FastAPI backend, which then uses the Mistral model (via Ollama) to determine the sentiment (Positive, Negative, or Neutral).") 