def calculate_score(hard, soft):
    final_score = (0.6 * hard) + (0.4 * soft)
    if final_score >= 80:
        verdict = "High"
    elif final_score >= 50:
        verdict = "Medium"
    else:
        verdict = "Low"
    return round(final_score, 2), verdict
