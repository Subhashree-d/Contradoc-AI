from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.contradiction import find_contradictions
from app.retriever import build_vectorstore
import shutil, os

app = FastAPI(title="ContraDoc AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    save_path = f"data/{file.filename}"
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": f"{file.filename} saved!"}

@app.post("/build")
async def build():
    try:
        build_vectorstore()
        return {"message": "Vector DB built with all documents!"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/analyze")
async def analyze(query: dict):
    result = find_contradictions(query["question"])
    return result

@app.get("/")
def root():
    return {"status": "ContraDoc AI is running!!"}