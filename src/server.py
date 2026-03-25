import os
import shutil
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from graph.stategraph import create_graph
from graph.state.graph_state import ResumeState
import uvicorn

app = FastAPI(title="Resume Evaluator API")

# Define upload folder (inside src/data/)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files (now at project root)
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/about")
async def get_about():
    return FileResponse(os.path.join(STATIC_DIR, "about.html"))

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.post("/evaluate")
async def evaluate_resume(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    # Save file
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
        return JSONResponse(content=result_state)
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
