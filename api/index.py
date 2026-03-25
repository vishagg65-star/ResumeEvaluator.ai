import os
import shutil
import json
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from src.graph.stategraph import create_graph
from src.graph.state.graph_state import ResumeState

app = FastAPI(title="Resume Evaluator API")

# Vercel Serverless: Only /tmp is writable
UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Path to static files
# ROOT_DIR is the root of the project
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_DIR = os.path.join(ROOT_DIR, "static")

# Mount static files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/about")
async def get_about():
    # Use fallback if static file not in local path (Vercel routes handled in vercel.json)
    path = os.path.join(STATIC_DIR, "about.html")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"error": "About page not found on local path"}, status_code=404)

@app.get("/")
async def read_index():
    path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(path):
        return FileResponse(path)
    return JSONResponse({"message": "Resume Evaluator API is running. Visit /about or the frontend UI."})

@app.post("/evaluate")
async def evaluate_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Save file to /tmp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(UPLOAD_DIR, f"resume_{timestamp}.pdf")
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Initialize State
    state: ResumeState = {
        "pdf_path": file_path,
        "target_role": role
    }

    # Create and Invoke Graph
    try:
        graph = create_graph()
        result_state = graph.invoke(state)
        # Cleanup /tmp after evaluation if desired
        try:
            os.remove(file_path)
        except:
            pass
        return JSONResponse(content=result_state)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
