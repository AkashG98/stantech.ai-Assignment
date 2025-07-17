from fastapi import FastAPI
from .routers import task

app = FastAPI(title="Task CRUD API")

app.include_router(task.router)
