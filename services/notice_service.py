from sqlalchemy.orm import Session
from models.notice import Notice
from schemas.notice_schema import NoticeCreate, NoticeUpdate
from datetime import datetime

def create_notice(db: Session, ca_id: int, data: NoticeCreate):
    notice = Notice(
        ca_id=ca_id,
        client_id=data.client_id,
        notice_type=data.notice_type,
        notice_date=data.notice_date,
        deadline=data.deadline,
        description=data.description,
        status="Received"
    )
    db.add(notice)
    db.commit()
    db.refresh(notice)
    return notice

def get_all_notices(db: Session, ca_id: int):
    return db.query(Notice).filter(Notice.ca_id == ca_id).all()

def get_notice(db: Session, notice_id: int, ca_id: int):
    return db.query(Notice).filter(
        Notice.id == notice_id,
        Notice.ca_id == ca_id
    ).first()

def update_notice(db: Session, notice_id: int, ca_id: int, data: NoticeUpdate):
    notice = get_notice(db, notice_id, ca_id)
    if not notice:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(notice, field, value)
    db.commit()
    db.refresh(notice)
    return notice

def delete_notice(db: Session, notice_id: int, ca_id: int):
    notice = get_notice(db, notice_id, ca_id)
    if not notice:
        return False
    db.delete(notice)
    db.commit()
    return True

def get_overdue_notices(db: Session, ca_id: int):
    today = datetime.today().strftime("%Y-%m-%d")
    notices = db.query(Notice).filter(
        Notice.ca_id == ca_id,
        Notice.status != "Responded"
    ).all()
    overdue = [n for n in notices if n.deadline < today]
    return overdue

def get_due_soon_notices(db: Session, ca_id: int):
    today = datetime.today().strftime("%Y-%m-%d")
    notices = db.query(Notice).filter(
        Notice.ca_id == ca_id,
        Notice.status != "Responded"
    ).all()
    due_soon = [n for n in notices if n.deadline >= today]
    return due_soon