from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

def hard_match(resume_text, jd_text):
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    return len(resume_words & jd_words) / len(jd_words) * 100

def soft_match(resume_text, jd_text):
    vectorizer = TfidfVectorizer().fit([resume_text, jd_text])
    vectors = vectorizer.transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity * 100
