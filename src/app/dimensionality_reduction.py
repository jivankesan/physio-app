# dimensionality_reduction.py
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.decomposition import PCA
import numpy as np

app = FastAPI()

class EmbeddingRequest(BaseModel):
    embeddings: list[list[float]]

@app.post("/reduce_dimensions")
async def reduce_dimensions(request: EmbeddingRequest):
    embeddings = np.array(request.embeddings)
    
    # Use PCA to reduce dimensions (example: from 1024 to 128)
    pca = PCA(n_components=128)
    reduced_embeddings = pca.fit_transform(embeddings)
    
    return {"reduced_embeddings": reduced_embeddings.tolist()}