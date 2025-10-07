<<<<<<< HEAD
from dotenv import load_dotenv
load_dotenv()
=======
from dotenv import load_dotenv; load_dotenv()
import os, json, time
import streamlit as st
import google.generativeai as genai

MODEL_ID = "gemini-2.5-flash"
>>>>>>> 85f87bd (new commit)
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

ATS_SCHEMA_EXAMPLE = {
  "type": "object",
  "properties": {
    "match_percent": {"type": "number", "minimum": 0, "maximum": 100},
    "summary": {"type": "string"}
  },
  "required": ["match_percent", "summary"],
  "additionalProperties": False
}

<<<<<<< HEAD
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
=======
HR_PROMPT = (
  "Role: You are an experienced technical recruiter.\n"
  "Task: Evaluate the resume against the job description.\n"
  "Output: strengths, gaps, and a fit verdict in <=120 words.\n"
  "Style: concise, specific, professional."
)

ATS_PROMPT = (
  "Role: You are an expert ATS and technical recruiter.\n"
  "Task: Read the Job Description and the Resume. Produce four sections with the exact keys below.\n"
  "Style: Be concise, specific, and evidence-aware. Do not repeat sentences across sections.\n"
  "Output: STRICT JSON ONLY with keys and types:\n"
  "{\n"
  '  "match_percent": 0-100 number,\n'
  '  "about_job": "string",\n'
  '  "your_resume": "string",\n'
  '  "summary": "string"\n'
  "}\n"
  "Definitions:\n"
  "- match_percent: ATS-style score 0–100, strict.\n"
  "- about_job: Explain what the job is, what they seek, and critical requirements from the JD.\n"
  "- your_resume: Analyze work experience, internships, and projects in detail. \
    Explain which experiences directly support this job’s requirements and which skills or experiences are missing. \
    Focus heavily on practical experience and achievements.\n"
  "- summary: Professional advice on changes to improve fit; do not copy from other sections.\n"
)


def upload_pdf_native(uploaded_file):
    """Upload PDF to Gemini API (not stored locally)."""
    return genai.upload_file(
        uploaded_file,
        mime_type="application/pdf",
        display_name=uploaded_file.name
    )
>>>>>>> 85f87bd (new commit)

def call_gemini(content_parts):
    """One retry wrapper."""
    model = genai.GenerativeModel(MODEL_ID)
    for i in range(2):
        try:
            return model.generate_content(content_parts, request_options={"timeout": 60})
        except Exception:
            if i == 1:
                raise
            time.sleep(1.5)

def parse_json(text: str):
    """Try to parse JSON, stripping fences if present."""
    try:
        return True, json.loads(text)
    except Exception:
        cleaned = text.replace("```json", "").replace("```", "").strip()
        try:
            return True, json.loads(cleaned)
        except Exception:
            return False, text
        
# ---------- UI
st.set_page_config(page_title="AI-Powered Resume Evaluator")
st.header("AI-Powered Resume Evaluator")

uploaded = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Job Description")
c1, c2 = st.columns(2)
hr_btn = c1.button("Tell Me About the Resume")
ats_btn = c2.button("Percentage match")

if uploaded: st.caption("PDF uploaded successfully.")

<<<<<<< HEAD
col1, col2 = st.columns(2)
with col1:
    submit1 = st.button("Tell Me About the Resume")

with col2:
    submit2 = st.button("Percentage match")

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The Repsonse is")
        st.write(response)
=======
if hr_btn or ats_btn:
    if not uploaded or not jd_text.strip():
        st.error("Upload a PDF and paste a job description.")
>>>>>>> 85f87bd (new commit)
    else:
        # Upload PDF to Gemini
        file_handle = upload_pdf_native(uploaded)

        # ---------- HR MODE ----------
        if hr_btn:
            try:
                with st.spinner("Analyzing your resume..."):
                    parts = [HR_PROMPT, "Job Description:\n" + jd_text, file_handle]
                    resp = call_gemini(parts)
                st.success("Analysis complete.")
                st.subheader("Response")
                st.write(resp.text)
            finally:
                try:
                    genai.delete_file(file_handle.name)
                except Exception:
                    pass

        # ---------- ATS MODE ----------
        if ats_btn:
            try:
                with st.spinner("Reading resume and job description... Please wait."):
                    parts = [
                        ATS_PROMPT + "\nReturn ONLY JSON.",
                        "Job Description:\n" + jd_text,
                        file_handle
                    ]
                    resp = call_gemini(parts)

                st.success("Evaluation complete.")
                ok, out = parse_json(resp.text)
                st.subheader("Response")

                if ok and isinstance(out, dict):
                    st.markdown("### Percentage match")
                    mp = out.get("match_percent", None)
                    st.write(f"{mp}%" if mp is not None else "")
                    
                    st.markdown("### About the job")
                    st.write(out.get("about_job", ""))

                    st.markdown("### Your resume")
                    st.write(out.get("your_resume", ""))

                    st.markdown("### Summary")
                    st.write(out.get("summary", ""))
                else:
                    cleaned = resp.text.replace("```json", "").replace("```", "").strip()
                    ok2, out2 = parse_json(cleaned)
                    if ok2 and isinstance(out2, dict):
                        st.markdown("### Percentage match");st.write(f'{out2.get("match_percent","")}%')
                        st.markdown("### About the job");   st.write(out2.get("about_job",""))
                        st.markdown("### About your resume");     st.write(out2.get("your_resume",""))
                        st.markdown("### Summary");         st.write(out2.get("summary",""))
                    else:
                        st.error("Model did not return valid JSON.")
                        st.code(resp.text)
            finally:
                try:
                    genai.delete_file(file_handle.name)
                except Exception:
                    pass
                