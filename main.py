from fastapi import FastAPI
from routes.user import router as auth_router

app = FastAPI(docs_url='/docs', redoc_url="/redoc")


app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}