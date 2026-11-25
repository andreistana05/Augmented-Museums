import os
import numpy as np
from PIL import Image
from embeddings import embed

ROOT = "data/reference"
vecs, labels = [], []

for exhibit_id in sorted(os.listdir(ROOT)):
    folder = os.path.join(ROOT, exhibit_id)
    if not os.path.isdir(folder):
        continue
    for f in sorted(os.listdir(folder)):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            vecs.append(embed(Image.open(os.path.join(folder, f))))
            labels.append(exhibit_id)

        print(exhibit_id, "->", labels.count(exhibit_id), "poze")

np.savez("index.npz", vecs = np.array(vecs), labels = np.array(labels))
print("Index salvat: ", len(labels), "vectori")
            