import google.generativeai as genai
import streamlit as st
import sys

# Try to get the API key
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    print("Error: GOOGLE_API_KEY not found in secrets.toml.")
    sys.exit(1)

# Configure the API
genai.configure(api_key=api_key)

print("API Key configured. Checking available models...")
try:
    found_model = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found supported model: {m.name}")
            found_model = True

    if not found_model:
        print("No models supporting generateContent were found for this API key.")

except Exception as e:
    print(f"Error communicating with the API. Please check your internet connection or API key validity.")
    print(f"Error details: {e}")