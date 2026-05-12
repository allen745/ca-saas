import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from schemas.document_schema import DocumentResponse
from services.document_service import save_document, get_documents, get_document
from core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/documents", tags=["Documents"])

security = HTTPBearer()

UPLOAD_DIR = "uploads"

def get_current_ca(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        ca_id = int(payload.get("sub"))
        return ca_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/upload/{client_id}", response_model=DocumentResponse)
def upload_document(
    client_id: int,
    doc_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    ca_id: int = Depends(get_current_ca)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_path = os.path.join(UPLOAD_DIR, f"{ca_id}_{client_id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    document = save_document(db, ca_id, client_id, file.filename, doc_type, file_path)
    return document

@router.get("/{client_id}", response_model=list[DocumentResponse])
def list_documents(client_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return get_documents(db, client_id, ca_id)

@router.get("/detail/{document_id}", response_model=DocumentResponse)
def get_one_document(document_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    document = get_document(db, document_id, ca_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document