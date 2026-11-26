import io
import json
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from embeddings import embed

THRESHOLD = 0.55
MARGIN = 0.05
MAX_VIEWS = 5

app = FastAPI()

data = np.load("index.npz")
REF_VECS = data["vecs"]
REF_LABELS = data["labels"]
with open("exhibits.json") as f:
    EXHIBITS = json.load(f)

def best_per_exhibit(query_vec):
    scores = REF_VECS @ query_vec
    best = {}
    for label, s in zip(REF_LABELS, scores):
        best[label] = max(best.get(label, -1.0), float(s))

    return best

@app.post("/api/identify")
async def identify(files: list[UploadFile] = File(...)):
    if not 1 <= len(files) <= MAX_VIEWS:
        raise HTTPException(400, f"Trimite intre 1 si {MAX_VIEWS} imagini")

    combined = {}

    for f in files:
        try:
            image = Image.open(io.BytesIO(await f.read()))
        except Exception:
            raise HTTPException(400, f"Imagine invalida")
        for label, s in best_per_exhibit(embed(image)).items():
            combined[label] = max(combined.get(label, -1.0), s)

        ranked = sorted(combined.items(), key = lambda x: -x[1])
        top_id, top_score = ranked[0]
        second = ranked[1][1] if len(ranked) > 1 else 0.0
        margin = top_score - second

        if top_score >= THRESHOLD and margin >= MARGIN:
            status = "identified"
        elif top_score >= THRESHOLD:
            status = "ambiguous"
        else:
            status = "unknown"

        exhibit = None
        if status == "identified":
            exhibit = EXHIBITS.get(top_id, {"name": top_id, "type": "3d",
                                        "description": "", "details": [],
                                        "mindTarget": None})
        return {
        "status": status,
        "id": top_id if status == "identified" else None,
        "score": top_score,
        "margin": margin,
        "views": len(files),
        "exhibit": exhibit,
        "top3": [{"id": i, "score": s} for i, s in ranked[:3]],
    }