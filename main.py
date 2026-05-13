from fastapi import FastAPI
from database import Base, engine
from routes.auth import router as auth_router
from routes.client import router as client_router
from routes.document import router as document_router
from routes.ai import router as ai_router
from routes.anomaly import router as anomaly_router
from routes.notice import router as notice_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CA SaaS API")

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(document_router)
app.include_router(ai_router)
app.include_router(anomaly_router)
app.include_router(notice_router)

@app.get("/")
def root():
    return {"message": "CA SaaS is running"}