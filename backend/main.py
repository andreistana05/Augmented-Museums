import io
import json
import numpy as np
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from embeddings import embed

THRESHOLD = 0.5

app = FastAPI()

data = np.load("index.npz")
REF_VECS = data["vecs"]
REF_LABELS = data["labels"]
with open("exhibits.json", "r") as f:
    EXHIBITS = json.load(f)

@app.post("/api/identify")
async def identity(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    scores = REF_VECS @ embed(image)
    best = {}

    for label, s in zip(REF_LABELS, scores):
        best[label] = max(best.get(label, -1.0), float(s))
        ranked = sorted(best.items(), key = lambda x : -x[1])

        top_id, top_score = ranked[0]
        known = top_score > THRESHOLD

    return {
        "known": known,
        "id": top_id if known else None,
        "score": top_score,
        "exhibit": EXHIBITS.get(top_id) if known else None,
        "top3": [{"id": i, "score": s} for i, s in ranked[:3]],
    }
 