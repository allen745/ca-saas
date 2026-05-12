from fastapi import FastAPI
from database import Base, engine
from routes.auth import router as auth_router
from routes.client import router as client_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CA SaaS API")

app.include_router(auth_router)
app.include_router(client_router)

@app.get("/")
def root():
    return {"message": "CA SaaS is running"}