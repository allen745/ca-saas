from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.notice_schema import NoticeCreate, NoticeUpdate, NoticeResponse
from services.notice_service import create_notice, get_all_notices, get_notice, update_notice, delete_notice, get_overdue_notices, get_due_soon_notices
from core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/notices", tags=["Notice Tracker"])

security = HTTPBearer()

def get_current_ca(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        ca_id = int(payload.get("sub"))
        return ca_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=NoticeResponse)
def add_notice(data: NoticeCreate, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return create_notice(db, ca_id, data)

@router.get("/", response_model=list[NoticeResponse])
def list_notices(db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return get_all_notices(db, ca_id)

@router.get("/overdue", response_model=list[NoticeResponse])
def overdue_notices(db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return get_overdue_notices(db, ca_id)

@router.get("/due-soon", response_model=list[NoticeResponse])
def due_soon_notices(db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return get_due_soon_notices(db, ca_id)

@router.get("/{notice_id}", response_model=NoticeResponse)
def get_one_notice(notice_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    notice = get_notice(db, notice_id, ca_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.put("/{notice_id}", response_model=NoticeResponse)
def edit_notice(notice_id: int, data: NoticeUpdate, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    notice = update_notice(db, notice_id, ca_id, data)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice

@router.delete("/{notice_id}")
def remove_notice(notice_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    success = delete_notice(db, notice_id, ca_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notice not found")
    return {"message": "Notice deleted successfully"}