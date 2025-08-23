import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("📊 AI-Powered Data Explorer")
st.write("Upload a CSV file to explore data, see visualizations, and run queries!")

# File uploader
uploaded_file = st.file_uploader("📂 Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Show preview
        st.subheader("👀 Data Preview")
        st.dataframe(df.head())

        # Summary stats
        st.subheader("📈 Dataset Summary")
        st.write(df.describe(include="all"))

        # Column visualization
        st.subheader("📊 Visualize a Column")
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

        # Query the data
        st.subheader("🔎 Query the Data")
        st.caption("Example: age > 30 & salary < 50000")
        query = st.text_input("Enter a condition:")

        if query:
            try:
                result = df.query(query)
                st.write(result)
                st.success(f"Returned {len(result)} rows.")
            except Exception as e:
                st.error(f"⚠️ Invalid query: {e}")

    except Exception as e:
        st.error(f"Error reading file: {e}")
