from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routes.ask import router as ask_router
from .routes.upload import router as upload_router
from .routes.notion_route import router as notion_router
from .routes.ask_image import router as ask_image_router



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ask_router)
app.include_router(upload_router)
app.include_router(notion_router)
app.include_router(ask_image_router)


# @app.get("/")
# def root():
#     return {"message": "Project ASTRA backend running"}
