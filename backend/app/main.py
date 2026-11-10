from fastapi import FastAPI

from app.database import Base, engine
from app.routers.messages import router as messages_router

app = FastAPI(
    title="SMS Service",
    description="SMS messaging service",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(messages_router)
