import streamlit as st
import os
import skills, llm, utils, ATS

# Initialize session state variables
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'job_description' not in st.session_state:
    st.session_state.job_description = ""
if 'skill_page' not in st.session_state:
    st.session_state.skill_page = {}
if 'ats_page' not in st.session_state:
    st.session_state.ats_page = {}
if "ats_results" not in st.session_state:
    st.session_state.ats_results = {}

st.set_page_config(page_title="Resume Analyzer", page_icon="🤖", layout="wide")

st.title("📄 Resume Analyzer")
st.write("Upload your resume and paste the job description to get insights")

# Create tabs
tabs = st.tabs(["🏠 Home", "🛠️ Skills Analysis", "📑 ATS Analysis"])

with tabs[0]:  # Home Tab
    st.header("Home")
    
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        resume_text = utils.get_resume_from_bytes(uploaded_pdf=uploaded_file)
        st.session_state.resume_text = resume_text
        st.success("Resume uploaded successfully!")
    
    st.session_state.job_description = st.text_area(
        "Paste the job description here:", height=200, value=st.session_state.job_description
    )
    
    if st.button("Analyze Resume"):
        if st.session_state.resume_text and st.session_state.job_description:
            st.success("Analysis started! Switch to Skills or ATS tab.")
        else:
            st.warning("Please upload a resume and provide a job description.")

with tabs[1]:  # Skills Analysis Tab
    st.header("Skills Analysis")
    
    if st.button("Run Skills Analysis"):
        model = llm.GroqModel()
        skills_section = skills.SkillsSection(
            Model_object=model, resume_text=st.session_state.resume_text, job_description=st.session_state.job_description
        )
        st.session_state.skill_page = skills_section.skill_analysis()
    
    if st.session_state.skill_page:
        with st.expander("🛠️ Your Current Skills", expanded=False):
            st.write(st.session_state.skill_page.get("curr_skills", "No skills found"))
        with st.expander("📋 Job-Required Skills", expanded=False):
            st.write(st.session_state.skill_page.get("job_skills", "No job skills found"))
        with st.expander("📈 Skills Gap Analysis", expanded=False):
            st.write(st.session_state.skill_page.get("comparision", "No analysis available"))
    else:
        st.info("Run skills analysis to see results.")

with tabs[2]:  # ATS Analysis Tab
    st.header("ATS Analysis")
    
    if st.button("Analyze Resume for ATS"):
        responses = ATS.analyze_resume(st.session_state.resume_text, st.session_state.job_description)
        st.session_state.ats_page = responses
        st.session_state.ats_results = responses
    
    if st.session_state.ats_page:
        with st.expander("🔍 Quick Scan", expanded=False):
            st.write(st.session_state.ats_results.get("quick_scan", "Quick scan not done"))
        with st.expander("🔍 Detailed Analysis", expanded=False):
            st.write(st.session_state.ats_results.get("detailed_analysis", "No detailed analysis"))
        with st.expander("📊 Resume Optimization Suggestions", expanded=False):
            st.write(st.session_state.ats_results.get("ats_optimization", "No analysis available"))
    else:
        st.info("Run ATS analysis to see results.")
