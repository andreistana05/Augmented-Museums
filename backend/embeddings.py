import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModel

MODEL_NAME = "facebook/dinov2-small"
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to(device).eval()

@torch.no_grad()
def embed(image: Image.Image) -> np.ndarray:
    inputs = processor(images = image.convert("RGB"), return_tensors = "pt").to(device)
    out = model(**inputs)
    vec = torch.nn.functional.normalize(out.last_hidden_state[:, 0], dim = -1)
    return vec.squeeze(0).cpu().numpy()