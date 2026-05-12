import fitz
import os
from sqlalchemy.orm import Session
from models.document import Document

UPLOAD_DIR = "uploads"


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def save_document(db: Session, ca_id: int, client_id: int, file_name: str, doc_type: str, file_path: str):
    extracted_text = extract_text_from_pdf(file_path)

    document = Document(
        ca_id=ca_id,
        client_id=client_id,
        file_name=file_name,
        file_path=file_path,
        doc_type=doc_type,
        extracted_text=extracted_text
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def get_documents(db: Session, client_id: int, ca_id: int):
    return db.query(Document).filter(
        Document.client_id == client_id,
        Document.ca_id == ca_id
    ).all()


def get_document(db: Session, document_id: int, ca_id: int):
    return db.query(Document).filter(
        Document.id == document_id,
        Document.ca_id == ca_id
    ).first()