from sqlalchemy.orm import Session
from models.client import Client
from models.document import Document


def check_anomalies(db: Session, ca_id: int):
    clients = db.query(Client).filter(Client.ca_id == ca_id).all()

    flagged = []

    for client in clients:
        issues = []

        documents = db.query(Document).filter(
            Document.client_id == client.id,
            Document.ca_id == ca_id
        ).all()

        if not documents:
            issues.append({
                "type": "NO_DOCUMENTS",
                "message": f"No documents uploaded for {client.full_name}"
            })

        for doc in documents:
            if doc.extracted_text:
                text = doc.extracted_text.lower()

                if "demand" in text or "penalty" in text:
                    issues.append({
                        "type": "DEMAND_OR_PENALTY",
                        "message": f"Document '{doc.file_name}' contains demand or penalty keywords"
                    })

                if "non-compliance" in text or "non compliance" in text:
                    issues.append({
                        "type": "NON_COMPLIANCE",
                        "message": f"Document '{doc.file_name}' mentions non-compliance"
                    })

                if "notice" in text and "income tax" in text:
                    issues.append({
                        "type": "IT_NOTICE",
                        "message": f"Document '{doc.file_name}' appears to be an income tax notice"
                    })

                if "tds" in text and "mismatch" in text:
                    issues.append({
                        "type": "TDS_MISMATCH",
                        "message": f"Document '{doc.file_name}' mentions TDS mismatch"
                    })

        if issues:
            flagged.append({
                "client_id": client.id,
                "client_name": client.full_name,
                "pan_number": client.pan_number,
                "issues": issues
            })

    return {
        "total_clients": len(clients),
        "flagged_clients": len(flagged),
        "flags": flagged
    }