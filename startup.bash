#!/bin/bash

uvicorn src.app.dimensionality_reduction:app --reload &  # Run in background
npm run dev &  # Run in background
npx convex dev &  # Run in background

wait  # Wait for all background processes to finish