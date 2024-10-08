from fastapi import FastAPI, File, UploadFile, Request  # Added Request import
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import json
from media.pose_wrapper import PoseAngleAnalyzer


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

# New endpoint to process video frame
@app.post("/process_frame_buffer")
async def process_frame_buffer(request: Request):
    # Parse the multipart form data
    form = await request.form()
    
    images = []  # List to hold the image arrays

    for file in form.getlist('file'):
        # Read the file content
        image_data = await file.read()
        
        # Convert the image data to a PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Convert the PIL Image to a NumPy array
        image_array = np.array(image)
        
        # Append the image array to the list
        images.append(image_array)

    if 'ref_angle' in form:
        ref_angle = json.loads(form['ref_angle'])
        
    analyzer = PoseAngleAnalyzer()
    analyzer.reference_angles = ref_angle

    feedback_data = []

    for frame in images:
        avg_live_angles, results = analyzer.process_live_frame(frame)
        joint_feedback = analyzer.compare_with_reference(avg_live_angles)

        # Store the feedback data of the current frame in a JSON structure
        feedback_frame = {joint_name: feedback for joint_name, feedback in zip(analyzer.joint_names, joint_feedback)}
        feedback_data.append(feedback_frame)

    return JSONResponse(content={"feedback_data": "feedback_data", "message": "Images processed successfully"})
