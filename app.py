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
You should act like an expert in the specified {field}.  You know what takes to be a 
good {position}. Your task is to evaluate the resume based on the given job description. 
1. You should extract the keywords from the {jd} and {text}. Then, compare the two sets of 
words and give your JD Match %.
2. You should summarise the resume in point form.  That is Profile Summary.
3. You should list all the keywords in the {jd} but not in {text} as Missing Keywords
4. You should suggest how to improve the resume's fit for the {position}. That is 
suggestion for improvement. 

field:{{field}}
position: {{position}}
description:{{jd}}
resume:{{text}}

I want the response in one single string having the structure

JD Match: {{JD Match}}% 
**Missing Keywords:**
{{Missing Keywords}}

**Profile Summary:**
{{Profile Summary}}

**Suggestions for Improvement:**
{{Suggestion for Improvement}}

The followings are important:
1. All the {{Missing Keywords}} must be actually found in {{jd}} 
but not in {{text}}. 
2. All the {{Suggestion for Improvement}} must be found in {{jd}} but not 
in {{text}}.
3. Do not mix up input_prompt with {{jd}} or {{text}}.
"""

## streamlit app
st.title("Smart Application Tracking System (ATS)")
st.text("Improve Your Resume ATS")
position = st.text_input("Enter your Position (e.g., junior software engineer, senior AI engineer, etc.)")
field = st.text_input("Enter the field (e.g., human resource, software engineering)")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader(
    "Upload Your Resume in PDF Format", type="PDF", help="Please upload the PDF"
)

submit = st.button("Submit")


if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        formatted_input_prompt = input_prompt.format(
            field=field, 
            position=position, 
            jd=jd, 
            text=text
        )
        response = get_gemini_response(formatted_input_prompt)
        st.subheader(response)


st.markdown("""
## Samples for Testing
- Sample Job Description: https://github.com/kkcheng72/ats20240416/blob/main/sample_jd.txt
- Sample CV (click the download icon on the right of the page): https://github.com/kkcheng72/ats20240416/blob/main/sample_cv.pdf
""")
