# dimensionality_reduction.py
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.decomposition import PCA
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your client origin for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmbeddingRequest(BaseModel):
    embeddings: list[list[float]]

@app.post("/reduce_dimensions")
async def reduce_dimensions(request: EmbeddingRequest):
    embeddings = np.array(request.embeddings)
    projection_matrix = np.random.rand(384, 24)

# Reduce dimensions by multiplying the embedding with the projection matrix
    reduced_embedding = np.dot(embeddings, projection_matrix)
    
    return {"reduced_embeddings": reduced_embedding.tolist()}