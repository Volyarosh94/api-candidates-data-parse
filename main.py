from fastapi import FastAPI
from routes.candidates import router


app = FastAPI()

app.include_router(router)
