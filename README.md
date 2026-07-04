# 📊 AI-Powered Data Explorer
AI-Powered Data Explorer is an interactive data analysis application built with Python, Streamlit, Pandas, and Matplotlib. Users can upload CSV datasets, explore them through interactive tables, generate summary statistics, visualize numerical features, and filter records without writing code.

Upload any CSV → instantly explore data with interactive tables, summary stats, and basic visualizations — built with **Python, Pandas, and Streamlit**.

## ✨ Features
- CSV upload & preview
- Summary statistics (`describe`)
- Histogram visualization for numeric columns
- Simple row filtering via query input
## Tech Stack

• Python
• Streamlit
• Pandas
• Matplotlib
## AI-Data-Explorer
│── app.py
│── titanic.csv
│── README.md
│── LICENSE
│── .gitignore

## 🚀 Quickstart
```bash
# 1) create & activate venv (optional but recommended)
# python -m venv .venv
# .venv\Scripts\activate

# 2) install deps
pip install streamlit pandas matplotlib

# 3) run the app
streamlit run app.py
