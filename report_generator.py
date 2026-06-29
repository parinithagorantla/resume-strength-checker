from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader(".")
)

template = env.get_template("report_template.html")

data = {
    "filename": "resume.pdf",
    "total": 77,
    "band": "Strong",

    "scores": [
        {
            "name": "Action Verbs",
            "value": 18,
            "max": 25,
            "detail": "Found 22 action verbs."
        },

        {
            "name": "Quantified Achievements",
            "value": 14,
            "max": 25,
            "detail": "9 bullets contain numbers."
        },

        {
            "name": "Formatting",
            "value": 22,
            "max": 25,
            "detail": "Good formatting overall."
        },

        {
            "name": "Skills",
            "value": 23,
            "max": 25,
            "detail": "Strong technical skills section."
        }
    ]
}

html = template.render(**data)

with open("resume_report.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Report generated!")