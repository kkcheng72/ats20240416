import streamlit as st
import google.generativeai as genai
from google.oauth2.service_account import Credentials
import os
import PyPDF2 as pdf
import json
# from dotenv import load_dotenv
# load_dotenv()


# Get your service account info from environment variables
service_account_info = json.loads(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# Create credentials from the service account info
credentials = Credentials.from_service_account_info(service_account_info)

# Configure the API with the created credentials
genai.configure(credentials=credentials)

## Gemini Pro Response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


## Prompt Template
input_prompt = """
Gemini should act like an experienced human resource person who is familiar with 
Application Tracking Systems.  Also, you are a skilled person in the relevant field 
knowing what takes to be a good {position}. Your task is to evaluate the resume 
based on the given job description, considering the current job market competitiveness. 
Provide suggestions to improve the resume's fit for the role. Assign the percentage 
matching based on job description and highlight missing keywords with high accuracy, 
prioritizing highly relevant skills and experience.

resume:{{text}}
description:{{jd}}
position: {{position}}

I want the response in one single string having the structure

JD Match: {{JD Match}}% 
**Missing Keywords:**
{{Missing Keywords}}

**Profile Summary:**
{{Profile Summary}}

**Suggestions for Improvement:**
{{Suggestion for Improvement}}

The followings are important:
1. All the suggested missing keywords must be actually found in the job description 
but not in the submitted resume. 
2. Profile summary is a summary of the submitted resume. 
3. The missing keywords must not be found in the profile summary.
4. All the suggestions for improvement are found in the job description but not 
in the submitted resume.
5. Do not mix up input_prompt with the job description or text from the resume.
"""

## streamlit app
st.title("Smart Application Tracking System (ATS)")
st.text("Improve Your Resume ATS")
position = st.text_input("Enter your Position (e.g., junior software engineer, senior AI engineer, etc.)")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader(
    "Upload Your Resume in PDF Format", type="PDF", help="Please upload the PDF"
)

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)
