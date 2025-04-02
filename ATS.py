import streamlit as st
import os
from dotenv import load_dotenv
# import google.generativeai as genai
from PyPDF2 import PdfReader
import llm
# GOOGLE_API_KEY = "AIzaSyD3DG2-SrRyglDn7YKFX5B04phweK3aQwI"
def analyze_resume(uploaded_file, job_description):
    """Processes the uploaded resume, analyzes it using Gemini AI, and returns the analysis result."""
    if uploaded_file is None:
        return "Please upload a resume to analyze."
    
    # Read PDF content
    # pdf_reader = PdfReader(uploaded_file)
    # pdf_text = "".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())
    pdf_text = uploaded_file
    # Define prompt based on analysis option
    prompts = {
        "quick_scan": f"""
        You are ResumeChecker, an expert in resume analysis. Provide a quick scan:
        1. Identify the most suitable profession.
        2. List 3 key strengths.
        3. Suggest 2 quick improvements.
        4. Give an overall ATS score out of 100.
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        
        "detailed_analysis": f"""
        You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis:
        1. Identify the most suitable profession.
        2. List 5 strengths.
        3. Suggest 3-5 areas for improvement.
        4. Rate aspects (Impact, Brevity, Style, Structure, Skills) out of 10.
        5. Review major sections (Summary, Experience, Education).
        6. Give an ATS score out of 100 with breakdown.
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        
        "ats_optimization": f"""
        You are ResumeChecker, an expert in ATS optimization. Provide optimization suggestions:
        1. Identify missing keywords.
        2. Suggest restructuring for ATS readability.
        3. Recommend changes for better keyword density.
        4. Provide 3-5 tailored resume improvement points.
        5. Give an ATS compatibility score out of 100.
        Resume text: {pdf_text}
        Job description: {job_description}
        """
    }
    
    # Load API key and configure Gemini AI
    # load_dotenv()
    # genai.configure(api_key=GOOGLE_API_KEY)#os.getenv("GOOGLE_API_KEY"))
    # model = genai.GenerativeModel("gemini-1.5-flash")
    model = llm.GroqModel()
    
    responses = {
        "quick_scan" : None,
        "detailed_analysis" : None,
        "ats_optimization" : None
        
    }
    for item in prompts:
        
        response = model.get_response(query= prompts[item], context= pdf_text)
        responses[item] = response
    print(responses)
    return responses


if __name__ == "__main__":
    # analyze_resume
    pass
