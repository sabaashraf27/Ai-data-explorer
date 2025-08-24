import google.generativeai as genai
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io # to implement Chatbot

# --- Configuration Section ---
# Configure the Google AI API with your key from secrets.toml
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"API Key not configured correctly. Please check your .streamlit/secrets.toml file. Error: {e}")

# --- Main App Interface ---
st.title("AI-Powered Data Explorer")
st.write("Upload a CSV file to explore data, see visualizations, and run queries!")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)
        st.success(" File uploaded successfully!")

        # --- Data Exploration & Visualization ---
        st.subheader(" Data Preview")
        st.dataframe(df.head())

        st.subheader(" Dataset Summary")
        st.write(df.describe(include="all"))

        st.subheader(" Visualize a Column")
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if numeric_cols:
            column = st.selectbox("Select a numeric column", numeric_cols)
            if column:
                fig, ax = plt.subplots()
                df[column].hist(ax=ax, bins=20, color="skyblue", edgecolor="black")
                ax.set_title(f"Distribution of {column}")
                st.pyplot(fig)
        else:
            st.warning("No numeric columns available for visualization.")

        st.subheader(" Query the Data")
        st.caption("Example: age > 30 & salary < 50000")
        query = st.text_input("Enter a condition:")

        if query:
            try:
                result = df.query(query)
                st.write(result)
                st.success(f"Returned {len(result)} rows.")
            except Exception as e:
                st.error(f" Invalid query: {e}")

        # --- AI-Powered Chatbot Integration ---
        st.header("Ask the AI about the Dataset")
        with st.expander("Start a Chat"):
            # Initialize chat history in session state
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Display past messages
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Handle user input
            if user_prompt := st.chat_input("Ask a question about the dataset..."):
                # Display user message and add to history
                with st.chat_message("user"):
                    st.write(user_prompt)
                st.session_state.chat_history.append({"role": "user", "content": user_prompt})

                # --- NEW CODE: Check for simple greetings ---
                greetings = ["hi", "hello", "hey", "namaste", "hola", "hi there"]
                
                if user_prompt.lower() in greetings:
                    assistant_response = "Hello there! I am your AI data analyst. How can I help you with this dataset today?"
                else:
                    # --- RAG: Retrieve and Augment ---
                    # Get dataset information to provide context to the model
                    buffer = io.StringIO()
                    df.info(buf=buffer, verbose=True)
                    dataset_info = buffer.getvalue()

                    # Construct the full prompt with context
                    full_prompt = (f"You are an expert data analyst. A user has uploaded a dataset with the following information:\n"
                                   f"```\n{dataset_info}```\n\n"
                                   f"The user's question is: '{user_prompt}'\n\n"
                                   f"Please provide a concise answer based ONLY on the provided dataset information. Do not make up data.")

                    # --- Call the Gemini model ---
                    try:
                        # Use gemini-1.5-flash as it's more widely available and has a higher quota
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(full_prompt)
                        assistant_response = response.text
                    except Exception as e:
                        assistant_response = "Sorry, I couldn't process that request. Please try again."
                        st.error(f"Error communicating with the model: {e}")

                # Display assistant's response and add to history
                with st.chat_message("assistant"):
                    st.write(assistant_response)
                st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        st.error(f"Error reading file. Please check if it's a valid CSV. Error: {e}")