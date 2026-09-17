import streamlit as st
from google import genai
import pypdf

st.title("AI Resume Screening Tool")
st.write("Welcome to the SafeX internship project interface!")

# Input fields for API key and Job Description
api_key = st.text_input("Enter your Gemini API Key", type="password")
job_description = st.text_area("Paste the Job Description Here")

# File uploader for the resume
uploaded_file = st.file_uploader("Upload a resume PDF", type=["pdf"])

if uploaded_file is not None and api_key and job_description:
    if st.button("Evaluate Resume"):
        with st.spinner("Analyzing resume against job description..."):
            try:
                # Extract text from the uploaded PDF
                reader = pypdf.PdfReader(uploaded_file)
                cleaned_resume = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        cleaned_resume += text + "\n"
                
                # Initialize Gemini client
                client = genai.Client(api_key=api_key)
                
                # Craft prompt
                prompt = f"""
                You are an expert technical recruiter. Evaluate the candidate's resume strictly against the job description below.

                JOB DESCRIPTION:
                {job_description}

                CANDIDATE RESUME:
                {cleaned_resume}

                Provide your response in the following format:
                1. Score: (Give a number from 1 to 100)
                2. Justification: (Write a short, 2-3 sentence explanation for the score)
                """
                
                # Generate response
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                )
                
                st.success("Evaluation Complete!")
                st.markdown("### AI Evaluation Result")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.info("Please enter your API key, paste a job description, and upload a PDF resume to enable evaluation.")
