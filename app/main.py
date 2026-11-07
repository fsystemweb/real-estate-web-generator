from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from app.models import PropertyData
from app.chains import generate_and_evaluate
from app.opik_sync import sync_to_opik
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_):
    sync_to_opik()  # create missing prompts and datasets in Opik
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-listing")
def generate_listing(property_data: PropertyData):
    try:
        return generate_and_evaluate(property_data)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 