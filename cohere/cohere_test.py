import pandas as pd
import numpy as np
import altair as alt
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import cohere

co = cohere.Client("2Y9RxsLFbrzbmKXFFHKWSURxZEvAoxuu8017E2fo") # Your Cohere API key

descriptions = [
    "Thigh lunge, medium difficulty, no equipment",
    "Calf raises, easy difficulty, no equipment",
    "Thigh stretch, hard difficulty, no equipment",
    "Thigh stretch, medium difficulty, no equipment",
    "Hip rotations, hard difficulty, no equipment",
    "Hip twists, hard difficulty, no equipment",
    "Thigh lift, medium difficulty, no equipment",
    "Thigh stretch, hard difficulty, no equipment",
    "Thigh squats, easy difficulty, no equipment",
    "Wrist extensions, easy difficulty, no equipment",
    "Hip raises, hard difficulty, no equipment",
    "Shoulder raises, easy difficulty, band"
]

def get_embeddings(texts, model='embed-english-v2.0'):
    response = co.embed(
        texts=texts,
        model=model,
        truncate='RIGHT'
    )
    return response.embeddings

embeddings = get_embeddings(descriptions)

def apply_pca(embeddings, n_components=None):
    embeddings = np.array(embeddings)  # Convert to NumPy array
    if n_components is None:
        # Maximum number of components is min(number of samples - 1, number of features)
        n_components = min(embeddings.shape[0] - 1, embeddings.shape[1])
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)
    return reduced_embeddings, pca

# Apply PCA to reduce dimensions
reduced_embeddings, pca = apply_pca(embeddings)

# Generate component names
component_names = [f'PC{i+1}' for i in range(reduced_embeddings.shape[1])]

# Create a DataFrame
df = pd.DataFrame(reduced_embeddings, columns=component_names)
df['Description'] = descriptions

# Save to CSV
df.to_csv('reduced_embeddings.csv', index=False)

print("Embeddings have been reduced and saved to 'reduced_embeddings.csv'")
