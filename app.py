from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_cotent,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="AI-Powered Resume Evaluator")

# Overwrite Style
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        h1, h2, h3 {
            color: #2e6f95;
            text-align: center;
        }
        .stTextArea textarea {
            border: 1px solid #ccc;
        }
        .stButton > button {
        background-color: #2e6f95;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5em 1em;
        transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #082534;
            color: white;
            border: none;
        }
        .stButton > button:active {
            background-color: #1c4d66;
            color: white !important;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

st.header("AI-Powered Resume Evaluator")
uploaded_file=st.file_uploader("Upload your Resume(PDF)",type=["pdf"])
input_text=st.text_area("Job Description: ",key="input")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

st.markdown("<p style='font-size: 16px;'>How would you like to evaluate your resume?</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Percentage match")


input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a professional-grade ATS (Applicant Tracking System) scanner designed to evaluate resumes with precision. 
Your task is to thoroughly examine the given resume **in detail**, comparing **every line and section** against the provided job description.
Provide the output: 
Match Percentage — Indicate how well the resume matches the job description.
Overall — In 1 or 2 lines, briefly summarize the overall alignment 

Do not list keywords, suggestions, or bullet points. Be concise and ATS-accurate.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the Resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the Resume")

