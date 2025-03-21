import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.session import get_db
from db.models import CandidateModel
from typing import Dict

from fastapi.responses import Response
import urllib.parse

from .utils import generate_pdf, parse_query

router = APIRouter()

logger = logging.getLogger(__name__)
@router.post("/submit-query")
def submit_query_endpoint(query: Dict[str, str], db: Session = Depends(get_db)):

    try:
        user_query = query.get("query")
        if not user_query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        skill_filters, min_experience = parse_query(user_query)
        query = db.query(CandidateModel)

        if skill_filters:
            query = query.filter(or_(*skill_filters))

        if min_experience:
            query = query.filter(CandidateModel.experience >= min_experience)

        candidates = query.limit(5).all()

        if not candidates:
            raise HTTPException(status_code=404, detail="No candidates found for the query")

        return [{
            "id": candidate.id,
            "name": candidate.name,
            "skills": candidate.skills,
            "experience": candidate.experience,
            "source": candidate.source
        } for candidate in candidates]

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the query")

@router.post("/generate-cv")
def generate_cv_endpoint(candidate_data: Dict[str, int], db: Session = Depends(get_db)):

    try:
        candidate_id = candidate_data.get("candidate_id")

        if not candidate_id:
            raise HTTPException(status_code=400, detail="Candidate ID is required")

        candidate = db.query(CandidateModel).filter(CandidateModel.id == candidate_id).first()

        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")

        buffer = generate_pdf(candidate)
        safe_filename = urllib.parse.quote(f"cv_{candidate.name.replace(' ', '_').replace('/', '_')}.pdf")
        headers = {"Content-Disposition": f"attachment; filename={safe_filename}"}

        return Response(content=buffer.read(), media_type="application/pdf", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the CV")
