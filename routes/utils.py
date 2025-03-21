import re
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from db.models import CandidateModel


def parse_query(user_query: str):
    words = user_query.split()
    experience_match = re.search(r'(\d+)\+?\s*years?', user_query, re.IGNORECASE)
    min_experience = experience_match.group(1) if experience_match else None

    skill_filters = [CandidateModel.skills.ilike(f'%{word}%') for word in words if word.lower() not in ["years", "year"]]

    return skill_filters, min_experience


def generate_pdf(candidate):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, f"CV: {candidate.name}")
    pdf.drawString(100, 730, f"Skills: {candidate.skills}")
    pdf.drawString(100, 710, f"Experience: {candidate.experience} year(s)")
    pdf.drawString(100, 690, f"Source: {candidate.source}")
    pdf.save()
    buffer.seek(0)

    return buffer