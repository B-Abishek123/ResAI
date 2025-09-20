from fastapi import FastAPI, UploadFile, Form
from app.utils.parser import parse_resume, parse_jd
from app.utils.matcher import hard_match, soft_match
from app.utils.scorer import calculate_score
from app.utils.feedback import generate_feedback

app = FastAPI(title="Automated Resume Relevance Checker")

@app.post("/evaluate/")
async def evaluate_resume(resume: UploadFile, jd: UploadFile):
    resume_text = parse_resume(await resume.read())
    jd_text = parse_jd(await jd.read())

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
