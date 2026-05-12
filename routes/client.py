from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.client_schema import ClientCreate, ClientUpdate, ClientResponse
from services.client_service import create_client, get_all_clients, get_client, update_client, delete_client
from core.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/clients", tags=["Clients"])

security = HTTPBearer()

def get_current_ca(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        ca_id = int(payload.get("sub"))
        return ca_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=ClientResponse)
def add_client(data: ClientCreate, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    client = create_client(db, ca_id, data)
    if not client:
        raise HTTPException(status_code=400, detail="PAN number already exists")
    return client

@router.get("/", response_model=list[ClientResponse])
def list_clients(db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    return get_all_clients(db, ca_id)

@router.get("/{client_id}", response_model=ClientResponse)
def get_one_client(client_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    client = get_client(db, client_id, ca_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def edit_client(client_id: int, data: ClientUpdate, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    client = update_client(db, client_id, ca_id, data)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/{client_id}")
def remove_client(client_id: int, db: Session = Depends(get_db), ca_id: int = Depends(get_current_ca)):
    success = delete_client(db, client_id, ca_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}