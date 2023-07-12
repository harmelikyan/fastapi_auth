import uvicorn
from fastapi import FastAPI
import api.v1 as v1

app = FastAPI()



app = FastAPI()

app.include_router(router=v1.router, prefix="/api/v1")






if __name__ == "__main__":
    uvicorn.run(app)