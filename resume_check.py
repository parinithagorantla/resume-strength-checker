import fitz
import argparse
import re
from jinja2 import Template
import os

print("Current working directory:", os.getcwd())

ACTION_VERBS = [
    "led",
    "built",
    "created",
    "designed",
    "developed",
    "implemented",
    "managed",
    "improved",
    "launched",
    "delivered"
]

def extract_text(pdf_path):

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text
def score_action_verbs(text):

    words = re.findall(r'\b\w+\b', text.lower())

    count = 0

    for word in words:

        if word in ACTION_VERBS:

            count += 1

    score = min(count, 25)

    detail = f"Found {count} action verbs"

    return score, 25, detail
def score_sections(text):
    sections = ["education", "experience", "projects", "skills"]

    text_lower = text.lower()

    found = 0

    for section in sections:
        if section in text_lower:
            found += 1

    score = found * 5   # max 20

    detail = f"Found {found}/4 sections"

    return score, 20, detail
def score_weak_phrases(text):
    phrases = [
        "hard worker",
        "team player",
        "responsible for",
        "worked on",
        "helped with"
    ]

    text_lower = text.lower()

    count = 0

    for phrase in phrases:
        if phrase in text_lower:
            count += 1

    score = max(15 - count * 3, 0)

    detail = f"Found {count} weak phrases"

    return score, 15, detail
def score_bullet_quality(text):
    lines = text.split("\n")

    bullets = [line for line in lines if "-" in line or "•" in line]

    if not bullets:
        return 0, 15, "No bullet points found"

    score = 0

    for b in bullets:
        words = len(b.split())

        if 8 <= words <= 20:
            score += 2
        elif words > 20:
            score += 1

    score = min(score, 15)

    detail = f"Analyzed {len(bullets)} bullet points"

    return score, 15, detail
def score_quantified(text):

    numbers = re.findall(r'\d+%|\d+\+?|₹\d+|\$\d+', text)

    count = len(numbers)

    score = min(count, 25)

    detail = f"Found {count} numerical achievements"

    return score, 25, detail
def generate_html_report(filename, av, q, s, w, b, total):
    with open("report_template.html", "r", encoding="utf-8") as file:
        template = Template(file.read())

    html = template.render(
        filename=filename,
        action_verbs=av,
        quantification=q,
        sections=s,
        weak_phrases=w,
        bullet_quality=b,
        total=total
    )

    with open("resume_report.html", "w", encoding="utf-8") as f:
        f.write(html)
parser = argparse.ArgumentParser(
    description="Resume Strength Checker"
)

parser.add_argument("pdf", help="Path to the resume PDF")

args = parser.parse_args()

text = extract_text(args.pdf)
av_score, av_max, av_detail = score_action_verbs(text)
q_score, q_max, q_detail = score_quantified(text)
s_score, s_max, s_detail = score_sections(text)
w_score, w_max, w_detail = score_weak_phrases(text)
b_score, b_max, b_detail = score_bullet_quality(text)

total = av_score + q_score + s_score + w_score + b_score
maximum = av_max + q_max + s_max + w_max + b_max


# =========================
# OUTPUT REPORT
# =========================
print("\n===== RESUME ANALYSIS REPORT =====\n")

print(f"Action Verbs     : {av_score}/{av_max} - {av_detail}")
print(f"Quantification   : {q_score}/{q_max} - {q_detail}")
print(f"Sections         : {s_score}/{s_max} - {s_detail}")
print(f"Weak Phrases     : {w_score}/{w_max} - {w_detail}")
print(f"Bullet Quality   : {b_score}/{b_max} - {b_detail}")

print("\n---------------------------")
print(f"TOTAL SCORE      : {total}/{maximum}")

generate_html_report(
    args.pdf,
    av_score,
    q_score,
    s_score,
    w_score,
    b_score,
    total
)

print("\nHTML report generated: resume_report.html")