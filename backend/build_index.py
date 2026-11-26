import os
import numpy as np
from PIL import Image
from embeddings import embed
import json

ROOT = "data/reference"
vecs, labels = [], []

for exhibit_id in sorted(os.listdir(ROOT)):
    folder = os.path.join(ROOT, exhibit_id)
    if not os.path.isdir(folder):
        continue
    count = 0
    for f in sorted(os.listdir(folder)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            vecs.append(embed(Image.open(os.path.join(folder, f))))
            labels.append(exhibit_id)
            count += 1
        print(exhibit_id, "->", labels.count(exhibit_id), "poze")
    print(f"{exhibit_id} -> {count} poze")
    if count < 5:
        print(f"Atentie: {exhibit_id} are putine poze de referinta")
np.savez("index.npz", vecs = np.array(vecs), labels = np.array(labels))
print("Index salvat: ", len(labels), "vectori")

with open("exhibits.json") as f:
    meta = json.load(f)

for ex in sorted(set(labels) - set(meta)):
    print(f"Atentie: {ex} are poze, dar nu are metadate in exhibits.json")

for ex in sorted(set(meta) - set(labels)):
    print(f"Atentie: {ex} are metdatae, dar nu are poze de referinta")