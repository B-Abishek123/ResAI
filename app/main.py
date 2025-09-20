# app/main.py (snippet)
# docx not working
# add pdf, docx support to JDs
# improve frontend ui


from fastapi import FastAPI, UploadFile, File
from app.utils.parser import parse_resume
from app.utils.matcher import hard_match, soft_match
from app.utils.scorer import calculate_score
from app.utils.feedback import generate_feedback

app = FastAPI(title="Automated Resume Relevance Checker")

@app.post("/evaluate/")
async def evaluate_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    resume_bytes = await resume.read()
    jd_bytes = await jd.read()

    resume_text = parse_resume(resume_bytes, resume.filename)
    jd_text = parse_resume(jd_bytes, jd.filename)  # reuse parse_resume for JD too

    hard = hard_match(resume_text, jd_text)
    soft = soft_match(resume_text, jd_text)
    final_score, verdict = calculate_score(hard, soft)
    feedback = generate_feedback(resume_text, jd_text)

    return {
        "hard_match": hard,
        "soft_match": soft,
        "final_score": final_score,
        "verdict": verdict,
        "feedback": feedback
    }
