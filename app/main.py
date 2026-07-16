from fastapi import FastAPI
from app.routers.projects import router as projects_router
from app.routers.elements import router as elements_router
from app.routers.calculations import router as calculations_router
from app.routers.materials import router as materials_router
from app.routers.users import router as users_router

app = FastAPI()

app.include_router(projects_router)
app.include_router(elements_router)
app.include_router(calculations_router)
app.include_router(materials_router)
app.include_router(users_router)