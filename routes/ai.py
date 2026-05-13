from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.document_service import get_document
from services.ai_service import summarize_document, draft_notice_reply, answer_question
from core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

security = HTTPBearer()


def get_current_ca(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        ca_id = int(payload.get("sub"))
        return ca_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


class QuestionRequest(BaseModel):
    question: str


@router.post("/summarize/{document_id}")
def summarize(document_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    document = get_document(db, document_id, ca_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not document.extracted_text:
        raise HTTPException(status_code=400, detail="No text found in document")

    summary = summarize_document(document.extracted_text)
    return {"summary": summary}


@router.post("/draft-reply/{document_id}")
def draft_reply(document_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    document = get_document(db, document_id, ca_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not document.extracted_text:
        raise HTTPException(status_code=400, detail="No text found in document")

    reply = draft_notice_reply(document.extracted_text)
    return {"draft_reply": reply}


@router.post("/ask/{document_id}")
def ask_question(document_id: int, request: QuestionRequest, db: Session = Depends(get_db),
                 ca_id: int = Depends(get_current_ca)):
    document = get_document(db, document_id, ca_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if not document.extracted_text:
        raise HTTPException(status_code=400, detail="No text found in document")

    answer = answer_question(document.extracted_text, request.question)
    return {"answer": answer}