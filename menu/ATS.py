import streamlit as st
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv
from streamlit_lottie import st_lottie 
import json
import os

load_dotenv()
genai.configure(api_key=os.getenv("OPENAI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def main():
    st.write("<h1><center>Applicant tracking systems</center></h1>", unsafe_allow_html=True)
    st.text("👉🏻                  Personal ATS for Job-Seekers & Recruiters                   👈")
    with open('src/ATS.json') as anim_source:
        animation = json.load(anim_source)
    st_lottie(animation, 1, True, True, "high", 200, -200)
    
    if 'is_logged' not in st.session_state:
        st.session_state['is_logged'] = False

    if st.session_state['is_logged']:
        st.text_input("Job Role")
        desc = st.text_area("Paste the Job Description")
        uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Pls Upload PDF file Only")
        submit = st.button("Submit")

        if submit:
            if uploaded_file is not None:
                reader = pdf.PdfReader(uploaded_file)
                text = ""
                for page_number in range(len(reader.pages)):
                    page = reader.pages[page_number] 
                    text += str(page.extract_text())

                input_prompt = f'''
                You're a skilled ATS (Applicant Tracking System) Scanner with a deep understanding of tech roles, software development, 
                tech consulting, and understand the ATS role in-depth. Your task is to evaluate the resume against the given description. 
                You must consider that the job market is crowded with applications and you should only pick the best talent. 
                Thus, assign the percentage & MissingKeywords with honesty & accuracy
                resume: {text}
                description: {desc}
                I want a output in one single string having the structure: {{"PercentageMatch": "%", "MissingKeywordsintheResume": [], "ProfileSummary": ""}}.
                '''

                with st.spinner("Evaluating Profile..."):
                    response = model.generate_content(input_prompt)
                response_data = json.loads(response.text)
                # st.write(response.text)

                st.subheader("ATS Scanner Dashboard")
                st.subheader("Candidate Evaluation Results")
                st.text(f"Percentage Match: {response_data['PercentageMatch']}")
                st.subheader("Missing Keywords in the Resume")
                for keyword in response_data['MissingKeywordsintheResume']:
                    st.text(keyword)
                st.subheader("Profile Summary")
                st.markdown(response_data['ProfileSummary'])
        if st.button("Logout"):
            st.session_state['is_logged'] = False
            del st.session_state['user']
            st.rerun()
    else:
        st.markdown("<h3 style='text-align: center; color: red;'>You are not Logged In</h3>", unsafe_allow_html=True)
