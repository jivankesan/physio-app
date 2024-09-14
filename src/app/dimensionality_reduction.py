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
    

    def apply_pca(embeddings, n_components=None):
        embeddings = np.array(embeddings)  # Convert to NumPy array
        if n_components is None:
            # Maximum number of components is min(number of samples - 1, number of features)
            n_components = min(embeddings.shape[0] - 1, embeddings.shape[1])
        pca = PCA(n_components=n_components)
        reduced_embeddings = pca.fit_transform(embeddings)
        return reduced_embeddings

    reduced_embeddings= apply_pca(embeddings, n_components=24)
    pca = PCA(n_components=24)
    reduced_embeddings = pca.fit_transform(embeddings)
    
    return {"reduced_embeddings": reduced_embeddings.tolist()}