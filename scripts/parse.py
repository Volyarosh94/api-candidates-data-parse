import re
import feedparser
from db.models import CandidateModel
from db.session import get_db
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

RSS_URL = os.getenv("RSS_URL")

KEYWORDS = [
    "Python", "Django", "Flask", "FastAPI", "Celery", "SQLAlchemy", "PostgreSQL", "MySQL", "MongoDB", "Redis",
    "pytest", "unittest", "Docker", "Kubernetes", "RabbitMQ", "Kafka", "AWS", "GCP", "Azure",
    "Git", "Linux", "GraphQL", "REST", "SOAP", "Microservices"
]


def parse_rss_feed(url: str):
    return feedparser.parse(url)


def extract_skills(description: str) -> str:
    skills = [tech for tech in KEYWORDS if tech.lower() in description.lower()]
    return ", ".join(skills)


def extract_experience(description: str) -> str:
    soup = BeautifulSoup(description, "html.parser")
    text = soup.get_text()

    match = re.search(r'(\d{1,2})(?:\+?)\s*(?:years?|роки?|рік|лет|год)', text, re.IGNORECASE)

    if match:
        return match.group(1)

    return "Experience is not specified"


def candidate_exists(db, name: str) -> bool:
    return db.query(CandidateModel).filter(CandidateModel.name == name).first() is not None


def save_candidate(db, name: str, skills: str, experience: str):
    new_candidate = CandidateModel(name=name, skills=skills, experience=experience)
    db.add(new_candidate)


def process_rss_feed():
    feed = parse_rss_feed(RSS_URL)
    db = next(get_db())

    for entry in feed.entries:
        name = entry.title
        if candidate_exists(db, name):
            continue

        skills = extract_skills(entry.description)
        experience = extract_experience(entry.description)

        save_candidate(db, name, skills, experience)

    db.commit()
    db.close()


if __name__ == "__main__":
    process_rss_feed()
