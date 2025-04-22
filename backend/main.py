from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from inference import generate_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/generated", StaticFiles(directory="generated"), name="generated")

class PromptRequest(BaseModel):
    prompt: str
    steps: int
    scale: float

@app.post("/generate")
async def generate(req: PromptRequest):
    filename = generate_image(req.prompt, req.steps, req.scale)
    return {"url": f"/generated/{os.path.basename(filename)}"}
