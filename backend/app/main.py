from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from app.services.parser import extract_text
from app.agents.graph import build_graph
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
graph = build_graph()

# Create audio directory and mount static files
os.makedirs("audio", exist_ok=True)
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


from fastapi import FastAPI, UploadFile, File, Form


@app.post("/upload")
async def upload(
    file: UploadFile = File(...),
    language_code: str = Form("en-IN"),
    speaker: str = Form("anushka")
):
    text = extract_text(file)

    state = {
        "text": text,
        "language_code": language_code,
        "speaker": speaker
    }
    result = graph.invoke(state)

    return {
        "fairness_score": result["summary"]["fairness_score"],
        "final_summary": result["summary"]["final_summary"],
        "key_takeaways": result["summary"]["key_takeaways"],
        "recommendation": result["summary"]["recommendation"],
        "pros": result["pros_cons"]["pros"],
        "cons": result["pros_cons"]["cons"],
        "hidden_risks": result["risks"]["hidden_risks"],
        "audio_url": f"/api/{result['audio_path']}",
        "clauses": result["clauses"]
    }
