from fastapi import FastAPI
from .routes.ask import router as ask_router
from .routes.upload import router as upload_router

app = FastAPI()

app.include_router(ask_router)
app.include_router(upload_router)


@app.get("/")
def root():
    return {"message": "Project ASTRA backend running"}
