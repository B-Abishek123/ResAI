def generate_feedback(resume_text, jd_text):
    missing = []
    for word in jd_text.split():
        if word.lower() not in resume_text.lower():
            missing.append(word)
    return {
        "missing_keywords": list(set(missing[:10])),
        "suggestion": "Consider adding missing skills/projects to improve your resume."
    }
