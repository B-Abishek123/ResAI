import streamlit as st
import requests

st.title("Automated Resume Relevance Checker")

resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])
jd = st.file_uploader("Upload Job Description", type=["txt"])

if st.button("Evaluate"):
    if resume and jd:
        response = requests.post(
            "http://127.0.0.1:8000/evaluate/",
            files={"resume": resume, "jd": jd}
        )
        result = response.json()
        st.json(result)
    else:
        st.warning("Please upload both Resume and JD")
