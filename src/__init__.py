import uvicorn
from fastapi import FastAPI
from src.books.routes import book_router
from src.db.main import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    print(f"server is starting ...")
    yield
    print(f"server has been stopped ...")

version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    lifespan=life_span
)
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])

if __name__ == '__main__':
    uvicorn.run('__main__:app', host='0.0.0.0', port=8000, reload=True)
