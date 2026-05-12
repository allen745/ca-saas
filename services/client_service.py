from sqlalchemy.orm import Session
from models.client import Client
from schemas.client_schema import ClientCreate, ClientUpdate

def create_client(db: Session, ca_id: int, data: ClientCreate):
    existing = db.query(Client).filter(Client.pan_number == data.pan_number).first()
    if existing:
        return None

    client = Client(
        ca_id=ca_id,
        full_name=data.full_name,
        pan_number=data.pan_number,
        email=data.email,
        phone=data.phone,
        entity_type=data.entity_type,
        assessment_year=data.assessment_year
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_all_clients(db: Session, ca_id: int):
    return db.query(Client).filter(Client.ca_id == ca_id).all()

def get_client(db: Session, client_id: int, ca_id: int):
    return db.query(Client).filter(Client.id == client_id, Client.ca_id == ca_id).first()

def update_client(db: Session, client_id: int, ca_id: int, data: ClientUpdate):
    client = get_client(db, client_id, ca_id)
    if not client:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int, ca_id: int):
    client = get_client(db, client_id, ca_id)
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True