from fastapi import FastAPI
from app.routers.projects import router as projects_router
from app.routers.elements import router as elements_router


app = FastAPI()

app.include_router(projects_router)
app.include_router(elements_router)