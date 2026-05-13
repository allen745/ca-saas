from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.anomaly_service import check_anomalies
from core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/anomaly", tags=["Anomaly Detection"])

security = HTTPBearer()

def get_current_ca(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        ca_id = int(payload.get("sub"))
        return ca_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/scan")
def scan_all_clients(db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    result = check_anomalies(db, ca_id)
    return result