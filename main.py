import uvicorn
from fastapi import FastAPI
import api.v1.endpoints as endpoints
from prometheus_fastapi_instrumentator import Instrumentator

# from db.database import create_connection

from db.models import get_db

# get_db()

# connection = create_connection("postgres", "postgres", "abc123", "127.0.0.1", "5432")
app = FastAPI()


app.include_router(router=endpoints.router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
